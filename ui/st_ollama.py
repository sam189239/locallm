import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from locallm.response import response_api

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}
model="llama3.2:1b"


def chat(prompt):
    response = response_api(prompt, st.session_state.chat_history, url=url, model=model, headers=headers)
    st.session_state.chat_history.append(prompt)
    st.session_state.chat_history.append(response)
    return response if response else "Error"

# Streamlit UI setup
st.set_page_config(page_title="PAI", layout="centered")
st.title("Locallm - Langchain")

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input field
user_input = st.chat_input("Type your message...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # Call the chat function (Replace with your actual function call)
    assistant_output = chat(user_input) 
    
    # Display assistant response
    st.session_state.messages.append({"role": "assistant", "content": assistant_output})
    with st.chat_message("assistant"):
        st.write(assistant_output)
if st.button('Clear history'):
    st.session_state.chat_history=[]
    st.session_state.messages = []


