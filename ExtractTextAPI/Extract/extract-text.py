import requests
from io import BytesIO
from PyPDF2 import PdfReader



def extract_data_from_url(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # Create a BytesIO object to hold the PDF content
        pdf_data = BytesIO(response.content)
        
        # Create a PdfReader object using the BytesIO object
        pdf_reader = PdfReader(pdf_data)
        
        # Process the PDF content
        for page in pdf_reader.pages:
            # Process each page of the PDF
            # Example: Print the page content
            print(page.extract_text())
        
        print("PDF content extracted successfully.")
    else:
        print("Failed to retrieve data from URL")

# Usage example
url = "https://extract-text-api.onrender.com/media/my_file/NUNSU01.pdf"
extract_data_from_url(url)