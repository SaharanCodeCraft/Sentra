from fastapi import FastAPI
from backend.api.decision import router as decision_router

app = FastAPI(
    title="SENTRA Backend",
    version="0.2.0",
    description="AI Policy Governance & Decision Intelligence Platform",
)

# Register API routes
app.include_router(decision_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}