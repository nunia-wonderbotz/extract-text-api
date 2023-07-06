import requests
from io import BytesIO
from PyPDF2 import PdfReader

# URL of the PDF file

root_url = 'http://127.0.0.1:8080/'
url = root_url+'media/my_file/NUNSU01.pdf'

# Download the PDF file
response = requests.get(url)
pdf_data = BytesIO(response.content)

# Create a PDF reader object
reader = PdfReader(pdf_data)

# Print the number of pages in the PDF file
n = len(reader.pages)
print(f"Number of pages in PDF file: {n}")

# Get the text from each page in the PDF file
for i in range(n):
    page = reader.pages[i]

    # Extract text from the page
    text = page.extract_text()
    print(f"Text on page {i+1}: {text}")