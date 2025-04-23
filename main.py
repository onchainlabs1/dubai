"""Streamlit UI for RE-Advisor – dashboard version (fixed order)."""

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from agent import REAdvisorAgent
from simulator import MarketSimulator

# ─────────────────── 0. CONFIG  ────────────────────────────────────
st.set_page_config(page_title="RE-Advisor", layout="wide")   # FIRST!

# ─────────────────── 1. ENV  ──────────────────────────────────────
load_dotenv()
GROQ_KEY   = os.getenv("GROQ_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MCP_URL    = os.getenv("MCP_SERVER_URL", "http://localhost:4000")
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

# ─────────────────── 2. INIT  ─────────────────────────────────────
sim   = MarketSimulator()
agent = REAdvisorAgent(
    openai_api_key=OPENAI_KEY,
    groq_api_key=GROQ_KEY,
    mcp_server_url=MCP_URL,
    simulator=sim,
)

if "history" not in st.session_state:
    st.session_state.history = []   # list[dict]

# ─────────────────── 3. SIDEBAR  ──────────────────────────────────
with st.sidebar:
    st.header("⚙ Settings")
    model = st.selectbox(
        "LLM model",
        ["llama3-8b-8192", "llama3-70b-8192", "gemma-7b-it"],
        index=0 if DEFAULT_MODEL == "llama3-8b-8192" else 1,
    )
    cycles = st.slider("Cycles to run", 1, 20, 1)
    auto   = st.checkbox("Auto-run on load", False)
    show_debug = st.checkbox("Show debug info", False)

    st.markdown("---")
    st.caption("Powered by **Groq Cloud** – blazing-fast inference  \nRiver online ML")

# ─────────────────── 4. MAIN TITLE  ───────────────────────────────
st.title("🏠 RE-Advisor – Agentic AI for Real-Estate")

# ─────────────────── 5. ACTION BUTTON  ────────────────────────────
run = st.button("Run decision cycle", type="primary") or auto
if run:
    for _ in range(cycles):
        state = sim.sample_state()
        action, rationale = agent.decide(state)
        result = sim.apply_action(state["id"], action)

        st.session_state.history.append(
            {
                "id": state["id"],
                "price": result["new_price"],
                "occupancy": result["occupancy"],
                "revenue": result["revenue"],
                "action": action,
                "rationale": rationale,
            }
        )

    latest = st.session_state.history[-1]

    # ── KPI metrics ───────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Price (AED)", f"{latest['price']:,}")
    col2.metric("🏢 Occupancy", f"{latest['occupancy']*100:.0f}%")
    col3.metric("📈 Monthly revenue", f"{latest['revenue']:,}")

    # ── Decision card ─────────────────────────────────────────────
    st.subheader("Latest decision")
    st.success(f"**{latest['action']}** — {latest['rationale']}")

    # ── History tabs ──────────────────────────────────────────────
    tab_table, tab_chart = st.tabs(["Table", "Revenue trend"])

    with tab_table:
        st.dataframe(pd.DataFrame(st.session_state.history))

    with tab_chart:
        df = pd.DataFrame(st.session_state.history)
        st.line_chart(df.set_index("id")["revenue"])

    # ── Debug info ────────────────────────────────────────────────
    if show_debug:
        with st.expander("Debug raw data"):
            st.json(
                {
                    "state": state,
                    "last_action": action,
                    "result": result,
                }
            )