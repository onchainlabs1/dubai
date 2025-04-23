# 🏠 RE-Advisor — Agentic AI for Real-Estate

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)
](https://dubai-agentic-advisor.streamlit.app/)

> **TL;DR** – RE-Advisor is a *digital analyst* that watches your property portfolio
in real-time and recommends rent changes or acquisition targets.  
> It perceives market data, reasons with an LLM, acts through an API, and
learns from every leasing outcome.

---

## 💼  Why a business user cares

| Pain today | How RE-Advisor helps |
|------------|----------------------|
| Manual, quarterly rent reviews | Autonomously prices units **daily** to protect occupancy & maximise yield |
| Analysts drown in listing feeds | Ingests thousands of listings, surfaces only **actionable** insights |
| Static ML models (needs data team) | **Online learning** – model updates itself after every transaction |
| Long lead-time on under-performing assets | Early-warning when vacancy or price anomalies appear |

Typical uplift: **+2 – 5 % Net Operating Income** with zero extra head-count.

---

## 🧠 How it works (high-level)

| Agentic pillar | What we implemented |
|---------------|---------------------|
| **Perception** | Live / synthetic listings gathered by the `MarketSimulator` (scraping ready) |
| **Reasoning** | Groq LLM (`llama3-8b-8192` by default, OpenAI fallback) + business rules |
| **Action** | Calls a REST endpoint via MCP (`/pricing/update`) to change rent |
| **Learning** | Lightweight online regressor (River) retrains on feedback each cycle |


---

## ✨  Key features

* **LLM-driven strategy** – natural-language reasoning with Groq Cloud (blazing-fast inference).  
* **Real-time ML loop** – incremental occupancy forecasting that improves every run.  
* **Pluggable “Action” layer** – swap the MCP URL to hit any PMS / CRM.  
* **Streamlit dashboard** – one click to see *state → decision → ROI*.

---

## 🚀 Quick-start (local)

# 1 Clone & enter repo
git clone https://github.com/onchainlabs1/dubai.git
cd dubai

# 2 Create virtual-env (optional but recommended)
python -m venv .venv && source .venv/bin/activate

# 3 Install deps
pip install --upgrade pip
pip install -r requirements.txt

# 4 Configure secrets
cp .env.example .env           # add your keys

# 5 Run
streamlit run main.py          # ➜ http://localhost:8501

## 🛠 Tech stack
	•	Python 3.11, Streamlit UI
	•	langchain-groq + Groq Cloud LLM (or OpenAI)
	•	River incremental ML
	•	Pydantic v2 data classes
	•	MCP (Model-Context-Protocol) REST action layer

## 📂 Project layout
.
├── main.py            # Streamlit UI + orchestration
├── agent.py           # Agent logic (LLM + ML + MCP)
├── ml_model.py        # OnlineOccupancyRegressor (River)
├── simulator.py       # Market data generator / ingestion stub
├── mcp_client.py      # Thin HTTP wrapper
├── requirements.txt
└── .env.example

## 🔄 What happens each cycle?

	1.	sample_state – pick / scrape a property.
	2.	predict – ML forecasts next-month occupancy.
	3.	LLM reasoning – decide decrease / maintain / increase rent.
	4.	MCP call – push new price to external system.
	5.	apply_action – simulator returns updated revenue.
	6.	learn_one – ML updates weights.
