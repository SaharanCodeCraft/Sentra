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
        default=None,
        description="Department related to the decision (HR, IT, Finance, etc.)"
    )

    urgency: Optional[str] = Field(
        default=None,
        description="Urgency level (low, medium, high)"
    )


class DecisionResponse(BaseModel):
    """
    Output schema for decision evaluation.
    """

    risk_level: str = Field(
        ...,
        description="Risk classification of the decision (Low, Medium, High)"
    )

    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score of the evaluation (0 to 1)"
    )

    policy_evidence: str = Field(
        ...,
        description="Relevant policy clauses or extracted evidence"
    )

    recommendation: str = Field(
        ...,
        description="Recommended action based on policy"
    )

    reasoning: str = Field(
        ...,
        description="Explanation of why the decision is classified at this risk level"
    )

    safer_alternative: str = Field(
        ...,
        description="Safer, policy-compliant alternative suggestion"
    )