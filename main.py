"""Streamlit entry-point for the RE-Advisor demo (English only)."""

import os
import streamlit as st
from dotenv import load_dotenv

from agent import REAdvisorAgent
from simulator import MarketSimulator

# ---------------------------------------------------------------------
# Environment variables
# ---------------------------------------------------------------------
load_dotenv()                                  # load values from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")   # optional fallback
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")     # primary LLM key
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:4000")

# ---------------------------------------------------------------------
# Init components
# ---------------------------------------------------------------------
simulator = MarketSimulator()
agent = REAdvisorAgent(
    openai_api_key=OPENAI_API_KEY,
    groq_api_key=GROQ_API_KEY,
    mcp_server_url=MCP_SERVER_URL,
    simulator=simulator,
)

# ---------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------
st.set_page_config(page_title="RE-Advisor Demo", layout="wide")
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