"""Core agent combining LLM reasoning, ML prediction and MCP actions."""
import json
from typing import Dict, Tuple

from langchain.chat_models import ChatOpenAI
from ml_model import OnlineOccupancyRegressor
from mcp_client import MCPClient

_PROMPT = """You are RE-Advisor, an autonomous real-estate strategist.

Goal: {goal}
Property state: {state}
Predicted occupancy (model): {prediction}
Historical feedback: {history}

Decide ONE action among ['decrease_price','maintain_price','increase_price'].
Return JSON with keys:
  action  – string
  reasoning – short string.
"""

class REAdvisorAgent:
    def __init__(self, openai_api_key: str, mcp_server_url: str, simulator):
        self.llm = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0.2,
            openai_api_key=openai_api_key,
        )
        self.model = OnlineOccupancyRegressor()
        self.mcp = MCPClient(server_url=mcp_server_url)
        self.simulator = simulator
        self.history = []

    def decide(self, state: Dict) -> Tuple[str, str]:
        pred = self.model.predict(state)
        prompt = _PROMPT.format(
            goal="maximize next-month ROI",
            state=json.dumps(state),
            prediction=pred,
            history=json.dumps(self.history[-5:]),
        )
        response = self.llm.predict(prompt)
        data = json.loads(response)

        # optional MCP call (e.g., update pricing DB)
        self.mcp.call(
            "pricing/update",
            {
                "property_id": state["id"],
                "new_price": self._new_price(state["price"], data["action"]),
            },
        )

        self.history.append({"state": state, "decision": data})
        return data["action"], data["reasoning"]

    @staticmethod
    def _new_price(price: float, action: str) -> float:
        if action == "decrease_price":
            return round(price * 0.95, 2)
        if action == "increase_price":
            return round(price * 1.05, 2)
        return price