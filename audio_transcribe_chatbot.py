import gradio as gr
import openai
import subprocess
OPENAI_API_KEY = "PASTE_KEY_HERE"
openai.api_key = OPENAI_API_KEY

messages = [{"role": "system", "content": 'You are a Finance advisor. Respond to all input in 250 words or less. Take input from valid and legitimate finance advisors'}]

def transcribe_and_chat(audio):
    global messages

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    subprocess.call(["say", system_message['content']])

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

app = gr.Interface(fn=transcribe_and_chat, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text")
app.launch()
