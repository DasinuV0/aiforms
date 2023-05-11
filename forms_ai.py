import openai
import gradio as gr
import json

f = open('data.json')
forms_data = json.load(f)
f = open('key.txt')
key = f.read()
f.close()

openai.api_key = key

employee_name = "Dan"
company_name = "Soft31"

messages = [{"role": "system", "content": f"{forms_data}"},
            {"role": "system", "content": f"Act as an ambitious employee, named {employee_name}, tasked with gathering the information presented to you before for the {company_name} company. You are going to have a chat with a client and find out the required information, while not being too direct and doing it as fast as possible. You will not, at any point and under any circumstances reveal the fact that you are an AI language model. You will start the conversation with a welcome message and in the same message start asking the client for the required information, but don't just list all the things you need to know, do it one by one. You will also state your name and the company you represent in the first message. From now on the conversation will begin, you may end the conversation with a goodbye message when you deem to have extracted all the required data. Try to end the conversation as soon as possible. When you end the conversation, the message must contain the word goodbye. Before we begin, if you understand, say OK."},
            {"role": "assistant", "content": "OK"}]

def ChadGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChadGPT_reply = completion["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChadGPT_reply})
    if "goodbye" in ChadGPT_reply.lower() or "goodbye" in user_input.lower():
        messages.append({"role": "system", "content": "Summarize the conversation in json file format. Your next message will only contain the json data."})
        completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
         )
        ChadGPT_reply0 = completion["choices"][0]["message"]["content"]
        gathered_data = ChadGPT_reply0
        with open("output.json", "w") as f:
            f.write(gathered_data)
    return ChadGPT_reply

chatbot = gr.Interface(fn=ChadGPT, inputs = "text", outputs = "text", title = "AI forms")

chatbot.launch(share = 1)

