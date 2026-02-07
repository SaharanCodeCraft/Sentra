from typing import Dict


class LLMClient:
    """
    Handles interaction with the language model.
    Responsible for reasoning and normalized output.
    """

    REQUIRED_FIELDS = {
        "risk_level": "Unknown",
        "policy_evidence": "",
        "recommendation": "",
        "reasoning": "",
        "safer_alternative": "",
    }

    def evaluate_decision(
        self,
        decision_text: str,
        policy_context: str
    ) -> Dict[str, str]:
        """
        Evaluate a decision using policy context and
        return normalized reasoning output.
        """

        # Placeholder reasoning logic (to be replaced by real LLM)
        raw_output = {
            "risk_level": "Medium",
            "policy_evidence": policy_context[:300],
            "recommendation": "Proceed with caution.",
            "reasoning": (
                "Based on the provided policy context, the decision "
                "may involve compliance considerations that require review."
            ),
            "safer_alternative": (
                "Consider an alternative approach that aligns more closely "
                "with documented policy guidelines."
            ),
        }

        return self._normalize_output(raw_output)

    def _normalize_output(self, output: Dict[str, str]) -> Dict[str, str]:
        """
        Ensures all required fields exist and are strings.
        """

        normalized = {}

        for key, default in self.REQUIRED_FIELDS.items():
            value = output.get(key, default)
            normalized[key] = str(value) if value is not None else default

        return normalized
