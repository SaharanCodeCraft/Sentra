from services.llm import LLMClient


class DecisionEngine:
    """
    Central orchestration layer for decision evaluation.
    """

    def __init__(self):
        self.llm = LLMClient()

    def evaluate(
        self,
        decision_text: str,
        policy_context: str | None = None
    ):
        if not decision_text or not decision_text.strip():
            raise ValueError("Decision text cannot be empty")

        policy_context = policy_context or (
            "No policy context retrieved yet. "
            "This will be populated via RAG."
        )

        return self.llm.evaluate_decision(
            decision_text=decision_text,
            policy_context=policy_context
        )
