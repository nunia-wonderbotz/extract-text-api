import requests
from io import BytesIO
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text_to_fp

url = "https://extract-text-api.onrender.com/media/my_file/NUNSU01.pdf"

response = requests.get(url)
if response.status_code == 200:
    pdf_data = BytesIO(response.content)
    text_data = BytesIO()
    extract_text_to_fp(pdf_data, text_data)
    text = text_data.getvalue().decode()
    print(text)
else:
    print("Failed to retrieve PDF file from the URL.")