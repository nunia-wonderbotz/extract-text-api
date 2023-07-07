import requests
from io import BytesIO
import io
from PyPDF2 import PdfReader

def extract_pdf_text(url):
    response = requests.get(url)
    response.raise_for_status()  # Check response status

    pdf_data = response.content
    pdf_stream = io.BytesIO(pdf_data)  # Convert to seekable stream
    reader = PdfReader(pdf_stream)

    page_texts = []
    for page in reader.pages:
        text = page.extract_text()
        page_texts.append(text)

    g_text = "\n".join(page_texts)
    return g_text

# Usage example
file = '/media/my_file/NUNSU01.pdf'
url = 'https://extract-text-api.onrender.com'
f_url = url + file
extracted_text = extract_pdf_text(f_url)
print(extracted_text)