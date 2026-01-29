from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="SENTRA Backend",
    description="AI Policy Governance & Decision Intelligence Platform",
    version="0.1.0"
)

# ---------- Health Check ----------
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------- Request Schema ----------
class DecisionInput(BaseModel):
    decision_text: str


# ---------- Response Schema ----------
class DecisionResponse(BaseModel):
    risk_level: str
    policy_evidence: str
    recommendation: str
    reasoning: str
    safer_alternative: str


# ---------- Evaluation Endpoint ----------
@app.post("/evaluate", response_model=DecisionResponse)
def evaluate_decision(payload: DecisionInput):
    """
    Evaluate a workplace decision against company policies.
    (ML logic will be added later)
    """

    return DecisionResponse(
        risk_level="Medium",
        policy_evidence="Relevant policy clauses will be listed here.",
        recommendation="Proceed with caution.",
        reasoning="This is a placeholder explanation.",
        safer_alternative="Consider a more policy-compliant alternative."
    )
