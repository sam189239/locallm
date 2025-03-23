import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
from locallm.response import response_lc
from langchain_community.chat_models import ChatOllama

model="llama3.2:1b"
llm = ChatOllama(model=model)
chat_history=[]

def chat(user_input):
    if user_input.strip().lower() == "/clear":
        return clear_history()
    global chat_history
    response, chat_history = response_lc(user_input, chat_history=chat_history, llm=llm, out=False)
    return response

## Gradio UI
def clear_history():
    global chat_history
    chat_history.clear()  # Reset the list
    return "Chat history cleared."

# demo = gr.Interface(
#     fn=chat,
#     inputs=gr.Textbox(lines=1, placeholder="Enter your prompt here..."),
#     outputs="text"
# )

with gr.Blocks() as demo:
    textbox = gr.Textbox(lines=1, placeholder="Enter your prompt here...")
    output = gr.Textbox()
    submit_btn = gr.Button("Send")
    clear_btn = gr.Button("Clear History")

    textbox.submit(chat, inputs=textbox, outputs=output)
    submit_btn.click(chat, inputs=textbox, outputs=output)
    clear_btn.click(clear_history, inputs=[], outputs=output)
    
demo.launch()