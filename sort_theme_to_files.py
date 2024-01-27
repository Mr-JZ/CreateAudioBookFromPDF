from openai import OpenAI

import json
import os
import pickle

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

with open("questions.pkl", "rb") as file:
    questions = pickle.load(file)


def chatgpt_prompt(question):
    prompt = f"""
    {question}
    Beantworte die Frage so genau wie moeglich, dabei sollte die Antwort nicht zu lang sein. 
    Die Antwort sollte Vorgelesen verstaendlich sein.
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4-0125-preview",
    )
    return chat_completion.choices[0].message.content


audio = []
for index, question in enumerate(questions):
    print(index, "/", len(questions))
    response = chatgpt_prompt(question)
    audio.append({"question": question, "answer": response})

with open("audio.json", "w") as outfile:
    json.dump(audio, outfile)
