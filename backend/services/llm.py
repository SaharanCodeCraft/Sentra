from typing import Dict

DECISION_PROMPT_TEMPLATE = """
You are an internal policy decision analyst.

Your task:
- Evaluate the given workplace decision strictly using the provided policy evidence.
- Do NOT assume facts not present in the policy evidence.
- If evidence is weak or missing, state uncertainty clearly.

Decision:
{decision_text}

Policy Evidence:
{policy_context}

Instructions:
1. Classify compliance risk as one of: Low, Medium, High.
2. Explain reasoning with direct reference to policy evidence.
3. Provide a clear recommendation.
4. Suggest a safer, policy-compliant alternative.

Respond ONLY in the following JSON format:
{{
  "risk_level": "<Low|Medium|High>",
  "policy_evidence": "<summary of relevant clauses>",
  "recommendation": "<recommended action>",
  "reasoning": "<clear explanation>",
  "safer_alternative": "<safer alternative>"
}}
"""
ALLOWED_RISK_LEVELS = {"Low", "Medium", "High"}


def normalize_risk_level(value: str, confidence: float | None = None) -> str:
    """
    Ensures risk level is valid and applies conservative defaults.
    """
    if not value:
        return "Medium"

    value = value.strip().capitalize()

    if value not in ALLOWED_RISK_LEVELS:
        return "Medium"

    # Conservative downgrade if confidence is low
    if confidence is not None and confidence < 0.5:
        return "High"

    return value



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

        prompt = DECISION_PROMPT_TEMPLATE.format(
            decision_text=decision_text,
            policy_context=policy_context
        )

        # Placeholder logic — real LLM call will replace this
        raw_output = {
            "risk_level": "Medium",
            "policy_evidence": policy_context[:300],
            "recommendation": "Proceed with caution.",
            "reasoning": (
                "The decision involves areas covered by the provided policy evidence. "
                "Potential compliance risks exist due to ambiguity."
            ),
            "safer_alternative": (
                "Adopt an approach explicitly allowed by policy to reduce risk."
            ),
        }

        return self._normalize_output(raw_output)


    def _normalize_output(self, output: Dict[str, str]) -> Dict[str, str]:
        normalized = {}

        risk = output.get("risk_level", "Medium")
        confidence = output.get("retrieval_confidence", None)

        normalized["risk_level"] = normalize_risk_level(risk, confidence)
        normalized["policy_evidence"] = str(output.get("policy_evidence", ""))
        normalized["recommendation"] = str(output.get("recommendation", ""))
        normalized["reasoning"] = str(output.get("reasoning", ""))
        normalized["safer_alternative"] = str(output.get("safer_alternative", ""))

        return normalized

    
    
