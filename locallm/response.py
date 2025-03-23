import requests
import json

def response_api(prompt, conversation_history = [], stream=False, url="http://localhost:11434/api/generate", model="llama3.2:1b", headers=None):
    if not headers:
        headers = {
            'Content-Type': 'application/json',
        }   
    conversation_history.append(prompt)

    full_prompt = "\n".join(conversation_history)

    data = {
        "model": model,
        "stream": stream,
        "prompt": full_prompt,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        conversation_history.append(actual_response)
        return actual_response
    else:
        print("Error:", response.status_code, response.text)
        return None
    
    
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
    
def response_lc(user_input, llm, chat_history=[], out=False, chat_prompt=None):

    if not chat_prompt:
        chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful and friendly AI assistant. Respond conversationally and helpfully. Here is the conversation history: {chat_history}"),
        ("user", "{user_input}")
    ])
    
    if not llm:
        llm = ChatOllama(model="llama3.2")
        
    messages = chat_prompt.format_messages(user_input=user_input, chat_history=chat_history)

    ## Can also simply use:
    # messages = [
    #     HumanMessage(content=user_input),
    # ]

    chat_history.append(HumanMessage(content=user_input))  

    response = llm.invoke(messages)  
    if out:
        response = []
        for chunk in llm.stream(messages):
            if type(chunk) == str:
                print(chunk, end="", flush=True)
                response.append(chunk)
            else:
                print(chunk.content, end="", flush=True)
                response.append(chunk.content)
        print()
        response = " ".join(response)
    else:
        response = llm.invoke(messages).content
    
    chat_history.append(AIMessage(response))  
    return response, chat_history