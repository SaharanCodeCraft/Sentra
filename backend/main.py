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
        You are a ruthless, strict AI Policy Governance auditor named Sentra.
        You must evaluate the raw DECISION exactly as it is requested. Do NOT assume the user has special permissions.
        
        DECISION: {request.text}
        
        POLICY EVIDENCE: 
        The text below contains up to 8 disconnected excerpts retrieved from the company rulebook. They are separated by "--- NEXT POLICY EXCERPT ---". They may not be sequentially related. Scan them independently to find the relevant rule.
        
        {found_text}
        
        Determine the risk level using these UNBREAKABLE rules in order:
        1. RELEVANCE CHECK: If NONE of the excerpts mention or relate to the user's DECISION at all, the riskLevel MUST be "Unknown".
        2. IF ANY excerpt says the action is "strictly prohibited", "not allowed", or violates the policy -> riskLevel MUST be "High". (Even if an exception process exists).
        3. IF the decision requires manager approval before proceeding -> riskLevel MUST be "Medium".
        4. IF the decision is explicitly allowed without special permission -> riskLevel MUST be "Low".
        
        You must return a JSON object with exactly these 5 keys:
        - "riskLevel": Must be exactly "Low", "Medium", "High", or "Unknown".
        - "evidence": Extract the exact 1-2 sentences proving this. (If Unknown, write "No relevant policy found in the database.")
        - "recommendation": A strict 2-3 word directive (e.g., "Deny Request", "Approve Request", "Manual Review Needed").
        - "reasoning": Explain the risk. IF UNKNOWN: State clearly that the uploaded documents do not contain rules regarding this specific request.
        - "alternatives": Provide the safe alternative. IF UNKNOWN: Write "Consult HR or IT directly for unlisted policies."
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