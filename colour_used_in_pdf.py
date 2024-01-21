import fitz  # Import PyMuPDF


def extract_text_colors(pdf_path):
    # Open the PDF
    doc = fitz.open(pdf_path)
    color_set = set()

    # Iterate through each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Extract text as a dictionary
        text_dict = page.get_text("dict")

        # Iterate through blocks, lines, and spans to extract color
        for block in text_dict["blocks"]:
            for line in block["lines"]:
                for span in line["spans"]:
                    if "color" in span:
                        color_set.add(span["color"])

    return color_set


# Example usage
pdf_path = "/home/mr-jz/Downloads/ITS Zusammenfassung.pdf"
colors_used = extract_text_colors(pdf_path)
for color in colors_used:
    print(color)
