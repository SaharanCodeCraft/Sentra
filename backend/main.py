import os
import shutil
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
    allow_origins=["*"], # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A. Configure the "Brain" (Embeddings)
# We use FastEmbed (runs on your CPU, no API key needed)
print("⏳ Loading AI Models... (This happens only once)")
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
Settings.llm = None

# B. Connect to Pinecone (The Database)
# PASTE YOUR KEY BELOW!
api_key = "pcsk_2ee6fs_M3qYXA2eA8MwyYGVpJKV4vLTw6py5nwNW3rWV9jxgcFBtxRQnxRwCjpnTZvStWH"
pc = Pinecone(api_key=api_key)
pinecone_index = pc.Index("sentra") # Matches your screenshot

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
        # Step 2: Read the text
        documents = SimpleDirectoryReader(input_files=saved_paths).load_data()
        
        # Step 3: Vectorize and Upload to Pinecone
        # This pushes the "math" of your PDF to the cloud
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


# --- 3. ENDPOINT: ANALYZE (Retrieval) ---
@app.post("/analyze")
async def analyze_scenario(request: AnalysisRequest):
    try:
        # Step 1: Connect to the existing Pinecone index
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

        # Step 2: Create a "Retriever" (Search Engine)
        # We ask for the top 1 most similar chunk of text
        retriever = index.as_retriever(similarity_top_k=1)
        
        # Step 3: Search!
        nodes = retriever.retrieve(request.text)
        
        if not nodes:
            return {
                "riskLevel": "Unknown",
                "evidence": "No relevant policy found.",
                "recommendation": "Manual Review Required",
                "reasoning": "The AI could not find any document matching this query.",
                "alternatives": "Check if the correct policy PDF was uploaded."
            }

        # Step 4: Extract the text found
        found_text = nodes[0].get_content()
        score = nodes[0].score # How confident is the match?

        # Step 5: Simple logic to guess Risk based on the text found
        # (Since we don't have GPT-4 to write a paragraph, we show the real policy text)
        risk = "Medium"
        if "prohibited" in found_text.lower() or "not allowed" in found_text.lower():
            risk = "High"
        elif "permitted" in found_text.lower() or "allowed" in found_text.lower():
            risk = "Low"

        return {
            "riskLevel": risk,
            "evidence": "Found in Knowledge Base (Pinecone)",
            "recommendation": "See Policy Extract Below",
            "reasoning": found_text[:500] + "...", # Show the first 500 chars of the actual PDF text
            "alternatives": "Consult the full document for more details."
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}