import fitz

import json

# 0 = black (maybe)
# 16711680 = red (don't learn)
# 28863 = blue (important)

black_tag = "maybe"
red_tag = "don't learn"
blue_tag = "important"
blue_rgb = 28863
red_rgb = 16711680
black_rgb = 0


def extract_colored_text(pdf_path, target_rgb):
    # Open the PDF
    doc = fitz.open(pdf_path)
    extracted_text = []

    # Iterate through each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Extract text as a dictionary
        text_dict = page.get_text("dict")

        # Iterate through blocks and lines
        bullet_points = False
        for block in text_dict["blocks"]:
            for line in block["lines"]:
                for span in line["spans"]:
                    if "color" in span and span["color"] == target_rgb:
                        if span["text"] != " " and bullet_points:
                            extracted_text.append(span["text"])
                            bullet_points = False
                        if span["text"] == "" or "-" or "\uf0b7":
                            bullet_points = True

    return extracted_text


# Example usage
zusammenfassung = []
pdf_path = "/home/mr-jz/Downloads/ITS Zusammenfassung.pdf"
blue_text = extract_colored_text(pdf_path, blue_rgb)
for text in blue_text:
    zusammenfassung.append({"text": f"{text}", "tag": "importend"})
black_text = extract_colored_text(pdf_path, black_rgb)
for text in black_text:
    zusammenfassung.append({"text": f"{text}", "tag": "maybe"})
print(zusammenfassung)
zusammenfassung_filter = [
    obj for obj in zusammenfassung if obj["text"] != "-" or "\uf0b7" or ".\t"
]

with open("zusammenfassung.json", "w") as outfile:
    json.dump(zusammenfassung_filter, outfile)
