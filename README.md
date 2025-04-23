🏠 RE‑Advisor — Agentic AI for Real‑Estate

RE‑Advisor is a hack‑ready prototype that demonstrates an agentic AI system — one that perceives, reasons, acts and learns autonomously — applied to real‑estate pricing and investment decisions.

Pillar

Implementation

Perception

Live/synthetic property data ingested via web‑scraping or API, parsed by the MarketSimulator.

Reasoning

An LLM (Groq mixtral‑8x7b‑32768 by default, fallback to OpenAI) analyses the current state & ML prediction to choose the next action.

Action

The agent calls a (mock) MCP endpoint to update the price and returns the decision to the UI.

Learning

A lightweight online regressor (river) continuously re‑trains on feedback after every cycle.

✨ Key Features

LLM‑driven strategy — natural‑language reasoning with Mixtral / Llama3.

Online ML loop — real‑time occupancy forecasting that improves with every step.

MCP integration — pluggable Action layer that can hit any REST endpoint (pricing engine, CRM, etc.).

Streamlit UI — one‑click demo; see state ➜ decision ➜ result JSON instantly.

Config in .env — switch LLM providers or MCP URLs without touching code.

🖼️ High‑level Architecture

┌────────────┐   state    ┌───────────┐
│ Simulator  │──────────▶│  Agent    │
│ (data)     │           │ (LLM+ML)  │
└────────────┘◀──────────│           │
          feedback/result└────┬──────┘
                               │ REST
                               ▼
                       ┌────────────────┐
                       │  MCP endpoint  │
                       └────────────────┘

🚀 Quick‑start (local)

# 1. Clone and enter the repo
$ git clone https://github.com/onchainlabs1/dubai.git
$ cd dubai

# 2. Create & activate a virtual environment (optional but recommended)
$ python3 -m venv .venv
$ source .venv/bin/activate

# 3. Install dependencies
$ pip install --upgrade pip
$ pip install -r requirements.txt

# 4. Configure secrets
$ cp .env.example .env   # then edit your keys

# 5. Run
$ streamlit run main.py  # http://localhost:8501

Required environment variables

Variable

Description

GROQ_API_KEY

Mandatory — key from https://console.groq.com.

OPENAI_API_KEY

Optional fallback for OpenAI models.

MCP_SERVER_URL

REST endpoint for pricing updates (http://localhost:4000 default).

☁️ Deploy on Streamlit Cloud (free)

Fork this repo, or point the deployment UI to onchainlabs1/dubai.

In Advanced settings → Secrets add:

GROQ_API_KEY = "gsk_live_…"
MCP_SERVER_URL = "http://your‑mcp.com"

Click Deploy. Streamlit installs requirements.txt and runs main.py automatically.

Share the public URL with the judges.

Alternative: Hugging Face Spaces (Gradio)

Create gradio_app.py (sample in docs/examples).

Add gradio to requirements.txt.

Push to a new Space → the demo is live in ~1 min.

🛠 Tech Stack

Python 3.10+

Streamlit – UI / demo layer

LangChain – LLM orchestration

Groq Cloud / OpenAI – language models

River – incremental ML

Pydantic v2 – data validation

MCP – dummy HTTP endpoint (replace with your backend)

📂 Repository layout

.
├── main.py            ← Streamlit entry‑point
├── agent.py           ← Agent logic (LLM + ML + MCP)
├── ml_model.py        ← OnlineOccupancyRegressor (River)
├── simulator.py       ← Market data generator / ingestion stub
├── mcp_client.py      ← Thin wrapper around HTTP POST
├── requirements.txt   ← Python dependencies
├── .env.example       ← Sample env‑vars
└── README.md          ← You are here

🔄 Feedback loop in detail

sample_state — pick (or scrape) a property record.

predict — ML model outputs expected occupancy.

LLM reasoning — Groq model decides decrease_price / maintain / increase.

MCP call — new price is sent to external system.

apply_action — simulator calculates new occupancy & revenue; feedback stored.

learn_one — ML model updates on the latest (features, target).

🤝 Contributing

Pull requests are welcome!  Please open an issue to discuss major changes first.Make sure pre‑commit passes and docs stay in English.

📜 License

This prototype is released under the MIT License — see LICENSE for details.

