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

# 1 Clone & enter repo
git clone https://github.com/onchainlabs1/dubai.git
cd dubai

# 2 (Create virtual-env)
python -m venv .venv && source .venv/bin/activate

# 3 Install deps
pip install -r requirements.txt

# 4 Configure secrets
cp .env.example .env   # edit your keys

# 5 Run
streamlit run main.py  # ⇒ http://localhost:8501

Required environment variables

Variable
Purpose
GROQ_API_KEY
Required â€” create at https://console.groq.com.
GROQ_MODEL
Optional â€” default llama3-8b-8192.
OPENAI_API_KEY
Optional fallback for OpenAI.
MCP_SERVER_URL
REST price endpoint (http://localhost:4000 default).

☁️ One-click deploy (Streamlit Cloud)

1. Fork or point Deploy-UI to onchainlabs1/dubai
2. Settings → Secrets
   GROQ_API_KEY   = "gsk_live_…"
   GROQ_MODEL     = "llama3-8b-8192"
   MCP_SERVER_URL = "https://your-mcp.io"
3. Click **Deploy** — Streamlit installs deps & runs main.py
4. Share the public URL with judges 🚀

🛠 Tech stack

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

