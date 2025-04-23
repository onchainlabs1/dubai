import json
import re
from typing import Dict, Tuple

JSON_BLOCK_RE = re.compile(r"\{.*\}", re.DOTALL)

# …

class REAdvisorAgent:
    # … __init__ stays the same …

    # ── Public API ─────────────────────────────────────────────
    def decide(self, state: Dict) -> Tuple[str, str]:
        """Perceive → reason → act → learn (robust JSON parsing)."""
        prediction = self.model.predict(state)

        prompt = _PROMPT.format(
            goal="maximize next-month ROI",
            state=json.dumps(state),
            prediction=prediction,
            history=json.dumps(self.history[-5:]),
        ) + "\n\nRespond ONLY with the JSON."

        response = self.llm.invoke(prompt)
        raw = response.content.strip()

        # -- robust JSON extraction --------------------------------------
        match = JSON_BLOCK_RE.search(raw)
        try:
            data = json.loads(match.group(0) if match else raw)
        except Exception:
            # fallback if parsing fails
            data = {"action": "maintain_price",
                    "reasoning": "Could not parse valid JSON."}

        # Action via MCP
        self.mcp.call(
            "pricing/update",
            {
                "property_id": state["id"],
                "new_price": self._new_price(state["price"], data["action"]),
            },
        )

        self.history.append({"state": state, "decision": data})
        return data["action"], data.get("reasoning", "")