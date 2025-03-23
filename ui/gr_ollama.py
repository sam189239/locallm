import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
from locallm.response import response_api

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}
model="llama3.2:1b"

conversation_history = []

def chat(prompt):
    if prompt.strip().lower() == "/clear":
        clear_history()
    response = response_api(prompt, conversation_history, url=url, model=model, headers=headers)
    conversation_history.append(prompt)
    conversation_history.append(response)
    return response if response else "Error"

## Gradio UI
def clear_history():
    conversation_history.clear()  # Reset the list
    return "Chat history cleared."

# demo = gr.Interface(
#     fn=chat,
#     inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
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