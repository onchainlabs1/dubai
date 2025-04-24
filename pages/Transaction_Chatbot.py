import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import time


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
FILE_ID = os.getenv("FILE_ID")

st.title("Dubai Real Estate Expert")
st.caption("Ask about property prices and trends")

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Process questions
if prompt := st.chat_input("Your question:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Thinking..."):
        try:
            # Create thread with data reference
            thread = client.beta.threads.create(
                messages=[{
                    "role": "user",
                    "content": prompt,
                    "attachments": [{
                        "file_id": FILE_ID,
                        "tools": [{"type": "code_interpreter"}]
                    }]
                }]
            )

            # Run analysis
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=ASSISTANT_ID
            )

            # Wait for completion
            while run.status not in ["completed", "failed"]:
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )

            if run.status == "failed":
                raise Exception(f"Analysis failed: {run.last_error}")

            # Get and display response
            messages = client.beta.threads.messages.list(thread.id)
            response = next(
                (m.content[0].text.value for m in messages.data 
                 if m.role == "assistant"),
                "Couldn't generate response"
            )
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

        except Exception as e:
            st.error(f"Error: {str(e)}")