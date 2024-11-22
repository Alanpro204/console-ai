from groq import Groq
from credentials import API_KEY
from configs import *

client = Groq(api_key=API_KEY)

messages = []


def complete():
    print("Assistant:\n->", end="")
    completion = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
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
    print("User:\n->", end="")
    entrada = input()
    message = {"role": "user", "content": entrada}
    messages.append(message)
    complete()
