from pydantic import BaseModel, Field
from typing import Optional

class DecisionInput(BaseModel):
    """
    Input schema for decision evaluation.
    """
    decision_text: str = Field(
        ...,
        min_length=10,
        description="Natural language description of the workplace decision"
    )

    department: Optional[str] = Field(
        None,
        description="Department related to the decision (HR, IT, Finance, etc.)"
    )

    urgency: Optional[str] = Field(
        None,
        description="Urgency level (low, medium, high)"
    )


class DecisionResponse(BaseModel):
    """
    Output schema for decision evaluation.
    """
    risk_level: str
    policy_evidence: str
    recommendation: str
    reasoning: str
    safer_alternative: str
