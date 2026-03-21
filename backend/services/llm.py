import requests
import json


class LLMClient:
    """
    Client to communicate with the local Ollama LLM server.
    """

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama3"

    def evaluate_decision(self, decision_text: str, policy_context: str):

        prompt = f"""
You are a policy compliance assistant.

You must evaluate the workplace decision using the policy evidence.

POLICY EVIDENCE:
{policy_context}

DECISION:
{decision_text}

IMPORTANT:
Return ONLY valid JSON.
Do NOT include explanations.
Do NOT include markdown.
Do NOT include text before or after JSON.

Output format:

{{
"risk_level": "Low | Medium | High",
"policy_evidence": "relevant policy text",
"recommendation": "recommended action",
"reasoning": "short explanation",
"safer_alternative": "safer compliant option"
}}
"""

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()["response"]

        # For now we return structured placeholders while testing
        result = response.json()["response"]
        try:
            parsed = json.loads(result)
            return parsed
        except Exception:
    # fallback if model returns bad format
    # 
           return {
               "risk_level": "Medium",
               "policy_evidence": policy_context,
               "recommendation": "Review policy guidelines before proceeding.",
               "reasoning": result,
               "safer_alternative": "Follow a clearly policy-approved process."
               }