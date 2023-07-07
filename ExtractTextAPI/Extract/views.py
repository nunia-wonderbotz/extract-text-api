from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import status
from Extract.models import Extract
from Extract.serializer import ExtractSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response

# importing required modules
from PyPDF2 import PdfReader
import requests
from io import BytesIO


# Index Page View
# def index(request):
#        return render(request, 'index.html')
   
# API Views
@api_view(['GET', 'POST', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def extract_list(request):
    if request.method == 'GET':
        extracts = Extract.objects.all()

        title = request.query_params.get('title', None)
        if title is not None:
            extracts = extracts.filter(title__icontains=title)

        extracts_serializer = ExtractSerializer(extracts, many=True)
        return Response(extracts_serializer.data)

    elif request.method == 'POST':
        extract_serializer = ExtractSerializer(data=request.data)
        if extract_serializer.is_valid():
            extract_serializer.save()
            # return Response(extract_serializer.data, status=status.HTTP_201_CREATED)
            
            

            # # Download the PDF file
            # response = requests.get(url)
            # pdf_data = BytesIO(response.content)

            # # Create a PDF reader object
            # reader = PdfReader(pdf_data)

            # # Print the number of pages in the PDF file
            # # n = len(reader.pages)
            # # print(f"Number of pages in PDF file: {n}")

            # # Extract text from each page of the PDF file
            # page_texts = []
            # for i in range(len(reader.pages)):
            #     page = reader.pages[i]
            #     text = page.extract_text()
            #     page_texts.append(f"Text on page {i+1}: {text}")

            # # Concatenate the text from all pages into a single string
            # g_text = "\n".join(page_texts)
            
            file = extract_serializer.data["file"]

            # # URL of the PDF file

            root_url = 'https://extract-text-api.onrender.com'
            url = root_url + file
            
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
                        # print(page.extract_text())
                        
                        # Return the response
                        return Response(page.extract_text(), status=status.HTTP_201_CREATED)
                    
                    print("PDF content extracted successfully.")
                else:
                    print("Failed to retrieve data from URL")

                # Usage example
                url = "https://extract-text-api.onrender.com/media/my_file/NUNSU01.pdf"
                extract_data_from_url(url)

            # # Return the response
            # return Response(g_text, status=status.HTTP_201_CREATED)
            
            # return Response(g_text, status=status.HTTP_201_CREATED)
        return Response(extract_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Extract.objects.all().delete()
        return Response({'message': '{} Extracts were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def extract_detail(request, pk):
    try:
        extract = Extract.objects.get(pk=pk)
    except Extract.DoesNotExist:
        return Response({'message': 'The extract does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        extract_serializer = ExtractSerializer(extract)
        return Response(extract_serializer.data)

    elif request.method == 'PUT':
        extract_serializer = ExtractSerializer(extract, data=request.data)
        if extract_serializer.is_valid():
            extract_serializer.save()
            return Response(extract_serializer.data)
        return Response(extract_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        extract.delete()
        return Response({'message': 'Extract was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def extract_list_published(request):
    extracts = Extract.objects.filter(published=True)

    if request.method == 'GET':
        extracts_serializer = ExtractSerializer(extracts, many=True)
        return Response(extracts_serializer.data)