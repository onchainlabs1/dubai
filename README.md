# 🏠 RE-Advisor — Agentic AI for Real-Estate
*A hack-ready prototype that **perceives, reasons, acts and learns** to optimise real-estate pricing & investments.*

---

## 🧩 Agentic pillars

| **Pillar**   | **What we implemented**                                                                                         |
|--------------|-----------------------------------------------------------------------------------------------------------------|
| Perception   | Live **or** synthetic listings gathered by the `MarketSimulator` (scraping/API-ready).                           |
| Reasoning    | Groq LLM (`llama3-8b-8192` default, fallback OpenAI) analyses state + ML prediction → chooses an action.          |
| Action       | Agent calls an **MCP** endpoint (`/pricing/update`) to update the price and returns the decision to the UI.      |
| Learning     | Online regressor (`river`) retrains after every feedback loop.                                                  |

---

## ✨ Key features

- **LLM-driven strategy** — natural-language decisions via Groq Llama-3.  
- **Online ML loop** — real-time occupancy forecasting that improves each cycle.  
- **MCP plug-in layer** — connect to any pricing engine / CRM via REST.  
- **Streamlit dashboard** — KPIs, decision card, history table & chart.  
- **`.env` config** — swap models or back-ends without touching code.

---

## 🖼️ Architecture (high-level)

```text
┌────────────┐   state    ┌───────────────────┐
│ Simulator  │──────────▶│   Agent (LLM)      │
│  /  Data   │           │  + ML + MCP        │
└────────────┘◀──────────│                   │
           feedback      └──────┬────────────┘
                                │  REST
                                ▼
                        ┌────────────────┐
                        │ MCP endpoint   │
                        └────────────────┘

#  🛠 Tech stack

Layer
Library / Service
UI
Streamlit
LLM
Groq Cloud (langchain-groq) Â· fallback OpenAI
Orchestration
LangChain Community
ML
River (online regression)
Validation
Pydantic v2
Action bus
MCP (HTTP wrapper)

📂 Repo layout

.
├── main.py            ← Streamlit dashboard entry-point
├── agent.py           ← Agent logic (LLM + ML + MCP)
├── ml_model.py        ← OnlineOccupancyRegressor (River)
├── simulator.py       ← Data generator / API stub
├── mcp_client.py      ← Tiny HTTP wrapper for MCP
├── requirements.txt   ← Python deps
├── .env.example       ← Sample env-vars
└── README.md          ← You are here

🔄 Feedback loop (6 steps)
	1.	sample_state → pick/scrape a property record
	2.	predict → ML model outputs expected occupancy
	3.	LLM reasoning → agent decides decrease / maintain / increase
	4.	MCP call → price update sent to external back-end
	5.	apply_action → simulator recomputes occupancy & revenue
	6.	learn_one → regressor updates online on fresh feedback

⸻

