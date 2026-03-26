from typing import Dict, Any
from backend.services.llm import LLMClient
from backend.rag.retriever import PolicyRetriever


class DecisionEngine:
    """
    Central orchestration layer for decision evaluation.
    Defines the contract between RAG and LLM.
    """

    def __init__(self):
        self.llm = LLMClient()
        self.retriever = PolicyRetriever()

    def _build_policy_context(self, rag_result: Dict[str, Any] | None) -> str:
        """
        Converts RAG output into a policy context string
        consumable by the LLM.
        """

        if not rag_result:
            return (
                "No policy evidence was retrieved. "
                "Decision must be evaluated conservatively."
            )

        evidence = rag_result.get("evidence", "")
        sources = rag_result.get("sources", [])
        confidence = rag_result.get("confidence", None)

        context = f"Policy Evidence:\n{evidence}\n\n"

        if sources:
            context += f"Sources: {', '.join(sources)}\n"

        if confidence is not None:
            context += f"Retrieval Confidence: {confidence}\n"

        return context

    def evaluate(
        self,
        decision_text: str,
        rag_result: Dict[str, Any] | None = None
    ) -> Dict[str, str]:
        """
        Main decision evaluation entry point.
        Handles RAG safety checks and forwards to LLM.
        """

        if not decision_text or not decision_text.strip():
            raise ValueError("Decision text cannot be empty")

        # --- Automatic Retrieval ---
        if rag_result is None:
            rag_result = self.retriever.retrieve(decision_text)

        # --- RAG Safety Checks ---
        confidence = rag_result.get("confidence", None)

        if confidence is not None and confidence < 0.4:
            rag_result["evidence"] = (
                "Policy retrieval confidence is low. "
                "Decision must be evaluated conservatively."
            )

        policy_context = self._build_policy_context(rag_result)

        llm_result = self.llm.evaluate_decision(
            decision_text=decision_text,
            policy_context=policy_context,
        )

        llm_result["policy_evidence"] = rag_result.get("evidence", "")

        return llm_result
        
        