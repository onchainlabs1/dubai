🏠 RE-Advisor — Agentic AI for Real‑Estate

RE‑Advisor is a hack‑ready prototype that demonstrates an agentic AI system — one that perceives, reasons, acts and learns autonomously — applied to real‑estate pricing and investment decisions.

Pillar

Implementation

Perception

Live/synthetic property data ingested via web‑scraping or API, parsed by the MarketSimulator.

Reasoning

An LLM (Groq mixtral‑8x7b‑32768 by default, fallback to OpenAI) analyses the current state & ML prediction to choose the next action.

Action

The agent calls an (MCP) endpoint to update the price and returns the decision to the UI.

Learning

A lightweight online regressor (river) continuously re‑trains on feedback after every cycle.

✨ Key Features

LLM‑driven strategy — natural‑language reasoning with Mixtral / Llama‑3.

Online ML loop — real‑time occupancy forecasting that improves with every step.

MCP integration — pluggable Action layer that can hit any REST endpoint (pricing engine, CRM, etc.).

Streamlit UI — one‑click demo; see state ➜ decision ➜ result JSON instantly.

Config in .env — switch LLM providers or MCP URLs without touching code.

🖼  Architecture (high‑level)

┌───────────┐  state   ┌───────────┐
│Simulator  │────────▶│  Agent    │
│(data)     │         │LLM+ML+MCP │
└───────────┘◀────────│           │
          feedback    └──┬────────┘
                          │ REST
                          ▼
                    ┌──────────────┐
                    │ MCP endpoint │
                    └──────────────┘

🚀 Quick‑start (local)

# 1. Clone and enter the repo (GitLab)
$ git clone https://gitlab.com/<your-namespace>/re_advisor.git
$ cd re_advisor

# 2. Create & activate a virtual environment (recommended)
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

Mandatory — key from https://console.groq.com.

OPENAI_API_KEY

Optional fallback for OpenAI models.

MCP_SERVER_URL

REST endpoint for pricing updates (http://localhost:4000 default).

☁️ Deploy with GitLab CI/CD + Streamlit Community Cloud

1 – GitLab repository setup

# after local changes
$ git remote set-url origin https://gitlab.com/<your-namespace>/re_advisor.git
$ git add .
$ git commit -m "Your message"
$ git push -u origin main  # triggers GitLab pipeline (optional)

You can create a simple .gitlab-ci.yml to build a Docker image or push the app to Streamlit Cloud.  For hack‑demos the fastest option is still Streamlit Cloud:

Go to https://share.streamlit.io/ → New app → point to your GitLab repo (<namespace>/re_advisor) instead of GitHub.

In Advanced settings → Secrets add:

GROQ_API_KEY = "gsk_live_…"
MCP_SERVER_URL = "http://your-mcp.com"

Click Deploy.  Streamlit installs requirements.txt and runs main.py automatically.

Share the public URL with stakeholders or judges.

🛠 Tech Stack

Python 3.10+

Streamlit – UI / demo layer

LangChain Community – LLM orchestration (Groq & OpenAI wrappers)

Groq Cloud  or OpenAI – language models

River – incremental ML

Pydantic v2 – data validation

MCP – pluggable REST action layer

📂 Repository layout

.
├── main.py            ← Streamlit entry‑point
├── agent.py           ← Agent logic (LLM + ML + MCP)
├── ml_model.py        ← OnlineOccupancyRegressor (River)
├── simulator.py       ← Market data generator / ingestion stub
├── mcp_client.py      ← Thin wrapper around HTTP POST
├── requirements.txt   ← Python dependencies
├── .env.example       ← Sample env‑vars
└── README.md          ← You are here

🔄 Feedback loop

sample_state — pick (or scrape) a property record.

predict — ML model outputs expected occupancy.

LLM reasoning — Groq model decides decrease_price / maintain / increase.

MCP call — new price is sent to external system.

apply_action — simulator calculates new occupancy & revenue; feedback stored.

learn_one — ML model updates on the latest (features, target).

🤝 Contributing

Fork on GitLab and submit a Merge Request.  Run pre-commit locally and keep all docs in English.

📜 License

Released under the MIT License — see LICENSE.

