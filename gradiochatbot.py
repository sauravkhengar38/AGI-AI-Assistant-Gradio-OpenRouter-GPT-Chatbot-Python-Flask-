import gradio as gr
from flask import Flask
import requests

API_KEY = ""   # <-- Put your OpenRouter API key

prompt = "This AI Chatbot\nAI: Hi, I am AI\nHuman: I am Human"

def get_output(message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Referer": "http://localhost",
        "X-Title": "Gradio Chatbot"
    }

    body = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": message}
        ],
        "temperature": 0.7
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=body
    ).json()

    try:
        return response["choices"][0]["message"]["content"]
    except:
        return f"Error: {response}"


def AGI_bot(input, history):
    history = history or []
    history.append({"role": "user", "content": input})

    output = get_output(input)
    history.append({"role": "assistant", "content": output})

    return history, history


with gr.Blocks() as block:
    gr.Markdown("<h1><center>AGI AI Assistant</center></h1>")

    chatbot = gr.Chatbot(type="messages")

    message = gr.Textbox(
        placeholder=prompt, 
        label="Type your message"
    )

    state = gr.State()
    submit = gr.Button("SEND")

    submit.click(AGI_bot, inputs=[message, state], outputs=[chatbot, state])

block.launch(debug=True)
