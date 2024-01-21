from PyPDF2 import PdfReader
from openai import OpenAI

import json
import os

with open("zusammenfassung_with_files.json", "r") as file:
    zusammenfassung = json.load(file)

file = PdfReader("/home/mr-jz/Downloads/ITS Verstaendnisfragen.pdf")
print(file.pages[0].extract_text())

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


def chat_gpt(aufgaben, filenames):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_from_text(aufgaben, filenames),
            }
        ],
        model="gpt-3.5-turbo-1106",
    )
    return chat_completion


# extract the question from the pdf
#   - look to lines if that is one ore two questions.
#       - if only one questions return it
#       - if two questions return the first one
#       - go one line down for each query
#       - add each question to a list
# sort the questions to the fitting files
