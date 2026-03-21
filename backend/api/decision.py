from fastapi import APIRouter
from backend.models.decision import DecisionInput, DecisionResponse
from backend.core.decision_engine import DecisionEngine

router = APIRouter()
engine = DecisionEngine()


@router.post("/evaluate", response_model=DecisionResponse)
def evaluate_decision(payload: DecisionInput):
    """
    Evaluate a workplace decision against company policies.
    """

    result = engine.evaluate(
        decision_text=payload.decision_text,
        rag_result=None  # RAG will be plugged in later
    )

    return DecisionResponse(**result)