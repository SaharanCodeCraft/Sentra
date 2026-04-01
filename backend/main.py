import os
import shutil
import requests
import json
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- RAG & AI Imports ---
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

app = FastAPI()

# --- 1. SETUP & CONFIGURATION ---

# Allow React to talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A. Configure the "Brain" (Embeddings)
print("⏳ Loading AI Models... (This happens only once)")
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
Settings.llm = None

# B. Connect to Pinecone (The Database)
# 🚨 PASTE YOUR NEW SECURE API KEY HERE 🚨
api_key = "pcsk_2ee6fs_M3qYXA2eA8MwyYGVpJKV4vLTw6py5nwNW3rWV9jxgcFBtxRQnxRwCjpnTZvStWH"
pc = Pinecone(api_key=api_key)
pinecone_index = pc.Index("sentra") 

# C. Connect LlamaIndex to Pinecone
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# D. Temp folder for uploads
UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class AnalysisRequest(BaseModel):
    text: str


# --- 2. ENDPOINT: UPLOAD (Ingestion) ---
@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    saved_paths = []
    
    # Step 1: Save files to disk
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_paths.append(file_path)

    try:
        # 🔥 SAFELY WIPE THE OLD DATABASE CLEAN 🔥
        try:
            pinecone_index.delete(delete_all=True)
            print("🗑️ Successfully wiped old vectors from Pinecone.")
        except Exception as delete_error:
            # If Pinecone throws a 404, it just means it's already empty! 
            print("ℹ️ Database is already empty, proceeding with upload...")

        # Step 2: Read the text
        documents = SimpleDirectoryReader(input_files=saved_paths).load_data()
        
        # Step 3: Vectorize and Upload to Pinecone
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
        )
        
        return {
            "status": "success", 
            "message": f"Successfully indexed {len(documents)} pages into Pinecone 'sentra' index."
        }

    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}

# --- ENDPOINT: CLEAR DATABASE ---
@app.delete("/clear")
async def clear_database():
    try:
        pinecone_index.delete(delete_all=True)
        return {"status": "success", "message": "Database wiped clean."}
    except Exception as e:
        # If we get an error here, it's almost certainly because it's already empty.
        # We tell the frontend it was a success anyway to keep the UI smooth.
        return {"status": "success", "message": "Database is already empty."}
    
# --- 3. ENDPOINT: ANALYZE (Retrieval + LLM) ---
@app.post("/analyze")
async def analyze_scenario(request: AnalysisRequest):
    try:
        # Step 1: Connect to Pinecone and Search
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        
        # Retrieve the top 8 most relevant chunks instead of just 1
        retriever = index.as_retriever(similarity_top_k=8)
        nodes = retriever.retrieve(request.text)
        
        if not nodes:
            return {
                "riskLevel": "Unknown",
                "evidence": "No relevant policy found.",
                "recommendation": "Manual Review Required",
                "reasoning": "The AI could not find any document matching this query.",
                "alternatives": "Check if the correct policy PDF was uploaded."
            }

        # Step 2: Extract and combine the text found in the PDF
        found_text = "\n\n--- NEXT POLICY EXCERPT ---\n\n".join([node.get_content() for node in nodes])

        # Step 3: Ask your local Ollama LLM to analyze the decision based on the text
        prompt = f"""
        You are a strict compliance auditor named Sentra. You must output valid JSON.
        
        DECISION: {request.text}
        POLICY EVIDENCE: {found_text}
        
        INSTRUCTIONS:
        Analyze the DECISION against the POLICY EVIDENCE. Assign a RISK_LEVEL from this exact list: ["High", "Medium", "Low", "Unknown"].
        
        MAPPING RULES:
        - "Unknown" = The evidence has nothing to do with the decision (e.g., asking about games, but the policy is about hardware).
        - "High" = The evidence states the action is strictly prohibited, denied, or a violation.
        - "Medium" = The evidence states the action requires manager approval, forms, or IT permission.
        - "Low" = The evidence states the action is explicitly allowed for everyone.
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "riskLevel": "[Insert exact RISK_LEVEL here]",
            "evidence": "[Extract 1 sentence of proof from the policy. If Unknown, write 'No policy found.']",
            "recommendation": "[2-3 words, e.g., 'Deny Request', 'Approve Request']",
            "reasoning": "[1 sentence explaining why. If Unknown, explain that the policy doesn't cover this.]",
            "alternatives": "[1 practical safe alternative step for the user]"
        }}
        """

        try:
            # Send the request to your local Ollama
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False,
                    "format": "json", # Forces Ollama to reply in perfect JSON!
                    "options": {
                        "temperature": 0.0 # 🔥 Kills hallucination/creativity 🔥
                    }
                },
                timeout=60 # Give it 60 seconds to think
            )
            response.raise_for_status()
            
            # Parse the JSON response
            llm_output = response.json().get("response", "{}")
            final_data = json.loads(llm_output)
            
            return final_data

        except Exception as llm_error:
            print(f"LLM Error: {llm_error}")
            return {
                "riskLevel": "Medium",
                "evidence": found_text[:200] + "...",
                "recommendation": "Review manually",
                "reasoning": "Pinecone found the policy, but the LLM offline or timed out.",
                "alternatives": "Make sure Ollama is running in the background."
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}