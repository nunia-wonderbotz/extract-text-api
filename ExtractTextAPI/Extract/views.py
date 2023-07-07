from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import status
from Extract.models import Extract
from Extract.serializer import ExtractSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from pdfminer.high_level import extract_text_to_fp

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
        file = request.FILES.get('file')

        # Read the file content and create a BytesIO object
        file_content = file.read()
        pdf_data = BytesIO(file_content)

        # Create a PDF reader object
        reader = PdfReader(pdf_data)

        # Extract text from each page of the PDF file
        page_texts = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            page_texts.append(f"Text on page {i+1}: {text}")

        # Concatenate the text from all pages into a single string
        extracted_text = "\n".join(page_texts)

        # Return the extracted text in the response
        response_data = {
            'text': extracted_text,
            'message': 'Text extracted successfully',
        }
        return Response(response_data, status=status.HTTP_200_OK)

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