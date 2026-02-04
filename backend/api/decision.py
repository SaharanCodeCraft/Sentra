from fastapi import APIRouter
from models.decision import DecisionInput, DecisionResponse

router = APIRouter()

@router.post("/evaluate", response_model=DecisionResponse)
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
