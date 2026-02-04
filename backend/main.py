from fastapi import FastAPI
from api.decision import router as decision_router

app = FastAPI(
    title="SENTRA Backend",
    description="AI Policy Governance & Decision Intelligence Platform",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(decision_router, prefix="/decision", tags=["Decision"])
