from groq import Groq
from openai import OpenAI
from credentials import API_KEY, PROXY, API_KEY_GROQ
from configs import *
import httpx
import os
from colorama import init, Fore
import base64
import webbrowser
init()
os.system("cls")

proxy_url = PROXY

client = OpenAI(api_key=API_KEY, http_client=httpx.Client(proxy=proxy_url))
#client = Groq(api_key=API_KEY_GROQ, http_client=httpx.Client(proxy=proxy_url))

messages = []


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def complete():
    model = "gpt-4o-mini"
    #model = "llama-3.2-90b-vision-preview"
    print(Fore.CYAN + model + ":\n->" + Fore.WHITE, end="")
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")

    print("\n")


while True:
    print(Fore.CYAN + "User:\n->" + Fore.WHITE, end="")
    entrada = ""
    images = []
    while True:
        linea = input()
        if linea == ".":
            break
        else:
            if linea.startswith("[img"):
                splited = linea.split(" ")
                img_uri = splited[1]
                images.append(img_uri)
            else:
                entrada += "\n" + linea
    content = []
    content.append({"type": "text", "text": entrada})
    for image in images:
        img = encode_image(image)
        content.append(
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}}
        )
    message = {"role": "user", "content": content}
    messages.append(message)
    complete()
