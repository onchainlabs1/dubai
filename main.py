"""Streamlit entry-point for RE-Advisor demo."""
import os
import streamlit as st
from agent import REAdvisorAgent
from simulator import MarketSimulator

st.set_page_config(page_title="RE-Advisor Demo", layout="wide")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:4000")

simulator = MarketSimulator()
agent = REAdvisorAgent(
    openai_api_key=OPENAI_API_KEY,
    mcp_server_url=MCP_SERVER_URL,
    simulator=simulator,
)

st.title("🏠 RE-Advisor – Agentic AI for Real-Estate")

if st.button("Run decision cycle"):
    state = simulator.sample_state()
    action, rationale = agent.decide(state)
    result = simulator.apply_action(state["id"], action)
    st.json(
        {
            "state": state,
            "action": action,
            "result": result,
            "rationale": rationale,
        }
    )