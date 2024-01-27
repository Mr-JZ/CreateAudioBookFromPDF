from openai import OpenAI


import json
import os

with open("zusammenfassung.json", "r") as file:
    zusammenfassung = json.load(file)

# next step is to read the folder with the vorlesungsskript
# dannach sortiere die dateien zu den themen

# Specify the directory path
directory_path = "/home/mr-jz/Nextcloud/Documents/hsos-osnabrueck/Semester_7/IT-Sicherheit/Vorlesung/"

# List all files and directories in the specified path
files_and_directories = os.listdir(directory_path)

# If you want only files and not directories, you can filter them
files = [
    f for f in files_and_directories if os.path.isfile(os.path.join(directory_path, f))
]

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def prompt_from_text(obj, filenames):
    # TODO: make it more efficient for the german language
    return f"""
    Ich gebe dir ein ein Objekt bei dem gibt es die felder Text und Tag. Du musst schauen welcher text in welcher Datei vorkommen kann. Geben nur die Dateien an bei der du dir sicher bist das hier der Text vorkommt.
    hier ist eine liste der Dateien:
    {filenames}
    Hier ist das Objekt:
    {obj}
    Die Antwort die zurueck gegeben werden soll, soll aus diesem Format erstellt werden, geben nur das ausgefuellte Format zurueck, hier ist der Kontext nicht so wichtig, kannst du alle Objecte nur im json fromat ausgeben und nicht mehr?:
    [{{ "thema": "<text>", "tag": "<tag>", "file": [<files>]}}, ... ]
    """


def chat_gpt(obj, filenames):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_from_text(obj, filenames),
            }
        ],
        model="gpt-4-0125-preview",
    )
    return chat_completion


json_data = []


response = chat_gpt(zusammenfassung, files).choices[0].message.content
try:
    json_obj = json.loads(response)
    print(json_obj)
    json_data.append(json_obj)
except ValueError:
    print(response)

# for obj in zusammenfassung:
#     response = chat_gpt(obj, files).choices[0].message.content
#     try:
#         json_obj = json.loads(response)
#         json_data.append(json_obj)
#     except ValueError:
#         print(response)
#
# with open("zusammenfassung_with_files.json", "w") as outfile:
#     json.dump(json_data, outfile)
