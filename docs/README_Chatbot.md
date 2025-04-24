# 🏙️ Dubai Real Estate AI Advisor

This is an interactive Streamlit app powered by OpenAI Assistants v2 that lets users query and analyze Dubai real estate transaction data using natural language. It includes geolocation features and intelligent code execution through a secure Assistant.

## What It Does

- Answers user questions about Dubai's real estate trends
- Performs Python-based analysis using the `code_interpreter` tool
- Uses geopy to geocode unknown locations when needed
- Built with OpenAI’s Assistant API (v2) and Streamlit
- Supports file searching and code generation for data questions


## How to Run Locally
This assumes you have access to the dataset and an OpenAI API key.

1. **Clone the repo**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/dubai.git
   cd dubai
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ASSISTANT_ID=your_assistant_id
   FILE_ID=your_uploaded_file_id
   ```

5. **Run the Streamlit app**:
   ```bash
   streamlit run pages/Transaction_Chatbot.py
   ```

## Deployment via Streamlit Cloud

If you're deploying this publicly on Streamlit Cloud:

1. Upload the code to a public GitHub repo.
2. Add your secrets to Streamlit Cloud's dashboard:
   - Go to https://streamlit.io/cloud
   - Under “Secrets”, add:
     ```
     OPENAI_API_KEY=...
     ASSISTANT_ID=...
     FILE_ID=...
     ```
3. Launch the app.

## Assistant Capabilities

This assistant can:
- Parse complex CSV schemas
- Run Python code on your data
- Use geopy to infer new areas in Dubai
- Answer questions without saying "based on the dataset"
