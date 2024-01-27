from openai import OpenAI

import pickle
import os
import json


with open("list_of_files.pkl", "rb") as file:
    files = pickle.load(file)

with open("questions.pkl", "rb") as file:
    questions = pickle.load(file)

prompt = f"""
    dateien: {files}
    fragen: {questions}
    Ordne die Fragen den Dateien zu:
    Dabei sollst du das in JSON Format machen:
    [{{
        "file": <file>,
        "fragen": [<frage1>, ...]
            }},
            ...]
            """


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-4-0125-preview",
)

response = chat_completion.choices[0].message.content
json_obj = {}
try:
    json_obj = json.loads(response)
except ValueError:
    print(response)

with open("zusammenfassung_with_files.json", "w") as outfile:
    json.dump(json_obj, outfile)
