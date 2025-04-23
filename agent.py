"""RE-Advisor Agent — Groq LLM + online ML + MCP action layer."""

from __future__ import annotations

import json
import os
import re
from typing import Dict, Tuple

# ─────────────────── LLM imports ──────────────────────────────
from langchain_groq import ChatGroq           # pip install langchain-groq

try:
    from langchain_community.chat_models import ChatOpenAI  # optional fallback
except ImportError:
    ChatOpenAI = None  # type: ignore  # noqa: N816

# ─────────────────── Local modules ────────────────────────────
from ml_model import OnlineOccupancyRegressor
from mcp_client import MCPClient

# ─────────────────── Prompt template ──────────────────────────
_PROMPT = """You are RE-Advisor, an autonomous real-estate strategist.

Goal: {goal}
Property state: {state}
Predicted occupancy (model): {prediction}
Historical feedback: {history}

Choose ONE action from ['decrease_price','maintain_price','increase_price'].
Return JSON with:
  action    : string
  reasoning : short string.
"""

_JSON_RE = re.compile(r"{.*}", re.DOTALL)


class REAdvisorAgent:
    """Combines LLM reasoning, online ML prediction and MCP action."""

    # ────── constructor ─────────────────────────────────────────
    def __init__(
        self,
        openai_api_key: str | None = None,
        groq_api_key: str | None = None,
        mcp_server_url: str = "http://localhost:4000",
        simulator=None,
    ):
        groq_model = os.getenv("GROQ_MODEL", "llama3-70b-8192")

        if groq_api_key:
            self.llm = ChatGroq(
                model_name=groq_model,
                groq_api_key=groq_api_key,
                temperature=0.2,
            )
        elif openai_api_key and ChatOpenAI is not None:
            self.llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                openai_api_key=openai_api_key,
                temperature=0.2,
            )
        else:
            raise ValueError(
                "Provide GROQ_API_KEY or OPENAI_API_KEY in the environment."
            )

        self.model = OnlineOccupancyRegressor()
        self.mcp = MCPClient(server_url=mcp_server_url)
        self.simulator = simulator
        self.history: list[dict] = []

    # ────── main public method ──────────────────────────────────
    def decide(self, state: Dict) -> Tuple[str, str]:
        """Perceive → reason → act → learn for one property."""
        prediction = self.model.predict(state)

        prompt = (
            _PROMPT.format(
                goal="maximize next-month ROI",
                state=json.dumps(state),
                prediction=prediction,
                history=json.dumps(self.history[-5:]),
            )
            + "\n\nRespond ONLY with the JSON."
        )

        raw = self.llm.invoke(prompt).content.strip()

        # Robust JSON extraction
        match = _JSON_RE.search(raw)
        try:
            data = json.loads(match.group(0) if match else raw)
        except Exception:
            data = {
                "action": "maintain_price",
                "reasoning": "No valid JSON parsed from LLM output.",
            }

        # Call MCP (example)
        self.mcp.call(
            "pricing/update",
            {
                "property_id": state["id"],
                "new_price": self._new_price(state["price"], data["action"]),
            },
        )

        self.history.append({"state": state, "decision": data})
        return data["action"], data.get("reasoning", "")

    # ────── helper ──────────────────────────────────────────────
    @staticmethod
    def _new_price(price: float, action: str) -> float:
        if action == "decrease_price":
            return round(price * 0.95, 2)
        if action == "increase_price":
            return round(price * 1.05, 2)
        return price