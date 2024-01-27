from elevenlabs import save, generate, set_api_key

import os
import json

test = False
have_to_offset = True
offset = 135

set_api_key(os.environ["ELEVENLABS_API_KEY"])

with open("audio.json", "r", encoding="utf-8") as f:
    audio = json.load(f)

# generate audio for the first question


def generator(text: str, file: str):
    # generate audio for the question
    # generate audio for the answer
    audio = generate(text=text, voice="Daniel", model="eleven_multilingual_v1")
    save(audio, file)


char_text = ""
text = "Dies ist die erste Frage: " + audio[0]["question"]
char_text += text
if not test and not have_to_offset:
    generator(text, "audio/0.wav")
    print(1, "/", len(audio))
# generate then the answer with the next question
start_index = 0
if have_to_offset:
    start_index = offset

for i in range(start_index, len(audio) - 1):
    # generate audio for the question
    # generate audio for the answer
    print(i + 2, "/", len(audio), f"creating the audiofile: audio/{i + 1}.wav")
    text = (
        "Die Antwort ist: "
        + audio[i]["answer"]
        + "Die nächste Frage ist: "
        + audio[i + 1]["question"]
    )
    char_text += text
    if not test:
        generator(text, "audio/" + str(i + 1) + ".wav")
    if i == 0 and test:
        break

if offset != len(audio) - 1:
    text = "Die Antwort ist: " + audio[len(audio) - 1]["answer"]
    char_text += text
    if not test:
        generator(text, "audio/" + str(len(audio)) + ".wav")
    print(
        len(audio), "/", len(audio), f"creating the audiofile: audio/{len(audio)}.wav"
    )
    print(
        "Char in the text:",
        len(char_text),
        "if it cost 0.33$ per 1000 char then it cost:",
        round(len(char_text) / 1000 * 0.33, 2),
        "$",
    )
