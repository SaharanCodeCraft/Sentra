import requests
import json
import re


class LLMClient:
    """
    Client to communicate with the local Ollama LLM server.
    Ensures structured and reliable JSON output.
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
You MUST return ONLY valid JSON.
You MUST include ALL fields.

"confidence_score" is REQUIRED and must be a number between 0 and 1.

Do NOT include explanations.
Do NOT include markdown.
Do NOT include text before or after JSON.

Output format:

{{
"risk_level": "Low | Medium | High",
"confidence_score": 0.0,
"policy_evidence": "relevant policy text",
"recommendation": "recommended action",
"reasoning": "short explanation",
"safer_alternative": "safer compliant option"
}}
"""

        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )

            response.raise_for_status()
            result = response.json().get("response", "")

            # 🔥 Extract JSON safely
            json_match = re.search(r"\{.*\}", result, re.DOTALL)

            if json_match:
                parsed = json.loads(json_match.group())

                # ✅ Ensure all fields exist (robust fallback)
                parsed.setdefault("risk_level", "Medium")
                parsed.setdefault("confidence_score", 0.7)
                parsed.setdefault("policy_evidence", policy_context)
                parsed.setdefault("recommendation", "Review policy guidelines.")
                parsed.setdefault("reasoning", "LLM response parsed.")
                parsed.setdefault("safer_alternative", "Follow a compliant process.")

                return parsed

            else:
                raise ValueError("No JSON found in LLM response")

        except Exception as e:
            # 🔥 Full fallback (never breaks API)
            return {
                "risk_level": "Medium",
                "confidence_score": 0.6,
                "policy_evidence": policy_context,
                "recommendation": "Review policy guidelines before proceeding.",
                "reasoning": f"LLM parsing failed: {str(e)}",
                "safer_alternative": "Follow a clearly policy-approved process."
            }