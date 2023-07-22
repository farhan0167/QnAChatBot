import requests
import io
from PyPDF2 import PdfReader

r = requests.get('https://abc.xyz/assets/9a/bd/838c917c4b4ab21f94e84c3c2c65/goog-10-k-q4-2022.pdf')

pdf_file = io.BytesIO(r.content)

# creating a pdf reader object
reader = PdfReader(pdf_file)

# printing number of pages in pdf file
print(len(reader.pages))

# getting a specific page from the pdf file
page = reader.pages[1]

# extracting text from page
text1 = page.extract_text()
print(text1)