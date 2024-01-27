from PyPDF2 import PdfReader
from openai import OpenAI

import json
import os
import ast
import pickle

with open("zusammenfassung_with_files.json", "r") as file:
    zusammenfassung = json.load(file)

file = PdfReader("/home/mr-jz/Downloads/ITS Verstaendnisfragen.pdf")

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def prompt_from_text(aufgaben, filenames):
    return f"""
    Kannst du die Fragen oder Aufgaben den Dateien zuordnen? Hier is es wichtig das die passenden sind. Also beschrenke dich. Wenn es nicht eine ganze Frage oder Aufgabe ist, dann nimm diese nicht mit rein.
    {filenames}
    Hier sind die Fragen oder Aufgaben:
    {aufgaben}
    You only give the answer in this format, try that is compilable json format:
    {{ "files": "<filenames>", "fragen": "<fragen>"}}
    """


def chat_gpt(prompt: str):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4",
    )
    return chat_completion


# extract the question from the pdf
#   - look to lines if that is one ore two questions.
#       - if only one questions return it
#       - if two questions return the first one
#       - go one line down for each query
#       - add each question to a list
# sort the questions to the fitting files
# questions = []
# for index, line in enumerate(text):
#     content = (
#         chat_gpt(prompt_is_a_combined_task(line, text[index + 1]))
#         .choices[0]
#         .message.content
#     )
#
#     if "#" in content:
#         continue
#     else:
#         print(content)
#         break
questions = []
for page in file.pages:
    chat_completion = chat_gpt(
        f"{page.extract_text()}\n Schreibe alle Fragen und Aufgaben raus. Und gebe diese in einer Python String liste wieder"
    )
    questions.extend(ast.literal_eval(chat_completion.choices[0].message.content))

print(questions)

with open("questions.pkl", "wb") as file:
    pickle.dump(questions, file)
