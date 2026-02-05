import os
import shutil
import time
import random
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# --- CONFIGURATION ---
# 1. Setup CORS so React can talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Define where we save files
UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 3. In-Memory "Database" of uploaded files
# We use this to make the mock answers look real by citing actual files you uploaded.
active_policies = []

class AnalysisRequest(BaseModel):
    text: str

# --- ENDPOINT 1: INGESTION (File Upload) ---
@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Saves uploaded files to disk and registers them in our 'active_policies' list.
    """
    global active_policies
    
    # Simulate processing time (Parsing PDF, Vectorizing...)
    time.sleep(2) 
    
    saved_count = 0
    
    for file in files:
        try:
            # 1. Create the full file path
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            
            # 2. Save the file to your hard drive
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # 3. Add to our active list if not already there
            if file.filename not in active_policies:
                active_policies.append(file.filename)
            
            saved_count += 1
            print(f"✅ Ingested: {file.filename}")
            
        except Exception as e:
            print(f"❌ Error saving {file.filename}: {e}")

    return {
        "status": "success", 
        "message": f"Successfully ingested {saved_count} documents into the Knowledge Base.",
        "active_files": active_policies
    }

# --- ENDPOINT 2: ANALYSIS (Decision Engine) ---
@app.post("/analyze")
async def analyze_scenario(request: AnalysisRequest):
    """
    Analyzes the text using Keyword Triggers and cites the uploaded files.
    """
    # Simulate AI "Thinking"
    time.sleep(1.5)
    
    text = request.text.lower()
    
    # Smart Source Selection:
    # If users uploaded files, pick one randomly to cite as evidence.
    # If not, fall back to a generic name.
    source_doc = random.choice(active_policies) if active_policies else "Corporate_Policy_v2.pdf"
    
    # --- LOGIC RULES ---
    
    # Scenario 1: High Risk (Security)
    if any(w in text for w in ["usb", "personal laptop", "dropbox", "secret", "password"]):
        return {
            "riskLevel": "High",
            "evidence": f"{source_doc} (Section 9.1 - Data Perimeter)",
            "recommendation": "Deny Request Immediately",
            "reasoning": "Detected unauthorized hardware/software usage. This violates data loss prevention protocols.",
            "alternatives": "Use the VDI Gateway or Company OneDrive."
        }

    # Scenario 2: Medium Risk (Remote Work)
    elif any(w in text for w in ["wifi", "coffee", "hotel", "airport", "vpn"]):
        return {
            "riskLevel": "Medium",
            "evidence": f"{source_doc} (Section 4.2 - Remote Access)",
            "recommendation": "Approve with Conditions",
            "reasoning": "Remote work is permitted, but public networks are insecure. Corporate VPN usage is mandatory.",
            "alternatives": "Use Company Cellular Hotspot if available."
        }

    # Scenario 3: Low Risk (General)
    else:
        return {
            "riskLevel": "Low",
            "evidence": f"{source_doc} (Section 1.0 - General Conduct)",
            "recommendation": "Automated Approval",
            "reasoning": "Request falls within standard operational guidelines.",
            "alternatives": "None required."
        }