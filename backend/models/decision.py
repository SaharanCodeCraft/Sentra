from pydantic import BaseModel, Field
from typing import Optional


class DecisionInput(BaseModel):
    """
    Represents a workplace decision scenario
    that needs to be evaluated against policy documents.
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
