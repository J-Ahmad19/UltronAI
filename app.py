import requests
import streamlit as st
import json
import os
api_key = os.environ["OPENROUTER_API_KEY"]


st.markdown(
    '''<div id="center-title"> <h1> Hi. I'm, <span style="color:#99ff00">UltronAI</span></h1> <p id="caption">How can I Help you today?</p></div>''',unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    
    #center-title {
        text-align: center;
        margin-top: 150px;

    }
    #caption {
        text-align:centre;
        
        }
    
    </style>
    """,
    unsafe_allow_html=True
)


if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])


# Get user input
prompt = st.chat_input("Ask me anything..")



if prompt:
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    

    # Placeholder for assistant’s streaming reply
    response_container = st.empty()
    full_reply = ""

    # OpenRouter request
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": st.session_state.messages,
        "stream": True,   # IMPORTANT: enable streaming
    }

    with requests.post(url, headers=headers, json=payload, stream=True) as r:
        for line in r.iter_lines():
            if line:
                decoded = line.decode("utf-8")
                if decoded.startswith("data: "):
                    data = decoded[6:]
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        token = chunk["choices"][0]["delta"].get("content", "")
                        full_reply += token
                        # Update typing animation
                        # Update typing animation
                        response_container.markdown(
                            f"<div style='color:#99ff00; font-weight:500;'>🤖 <b>UltronAI:</b> {full_reply}</div>",
                            unsafe_allow_html=True
                         )

                    except Exception:
                        pass

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": full_reply})
   
