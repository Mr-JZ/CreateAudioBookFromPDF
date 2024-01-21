from PyPDF2 import PdfReader

reader = PdfReader("/home/mr-jz/Downloads/ITS Zusammenfassung.pdf")

number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()
print(text, page, number_of_pages)
