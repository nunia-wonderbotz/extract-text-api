from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import status
from OCR.models import OCR
from OCR.serializer import OCRSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from pdfminer.high_level import extract_text_to_fp

# importing required modules
from PyPDF2 import PdfReader
import requests
from io import BytesIO

# base 64 required modules
import base64
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:/Users/SunilNunia/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"

# Create your views here.

# API Views
@api_view(['GET', 'POST', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def ocr_list(request):
    if request.method == 'GET':
        ocrs = OCR.objects.all()

        title = request.query_params.get('title', None)
        if title is not None:
            ocrs = ocrs.filter(title__icontains=title)

        ocrs_serializer = OCRSerializer(ocrs, many=True)
        return Response(ocrs_serializer.data)

    elif request.method == 'POST':
        base64_data = request.data.get('base64_data')

        # Decode base64 data and create a BytesIO object
        # file_content = base64.b64decode(base64_data)
        # pdf_data = Image.open(BytesIO(file_content))

        # # Perform OCR on the PDF file
        # text = pytesseract.image_to_string(pdf_data, lang='eng')

        # Return the extracted text in the response
        response_data = {
            'text': base64_data,
            'message': 'Text extracted successfully!',
        }
        return Response(response_data, status=200)

    elif request.method == 'DELETE':
        count = OCR.objects.all().delete()
        return Response({'message': '{} OCRs were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def ocr_detail(request, pk):
    try:
        ocr = OCR.objects.get(pk=pk)
    except OCR.DoesNotExist:
        return Response({'message': 'The ocr does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ocr_serializer = OCRSerializer(ocr)
        return Response(ocr_serializer.data)

    elif request.method == 'PUT':
        ocr_serializer = OCRSerializer(ocr, data=request.data)
        if ocr_serializer.is_valid():
            ocr_serializer.save()
            return Response(ocr_serializer.data)
        return Response(ocr_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ocr.delete()
        return Response({'message': 'OCR was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def ocr_list_published(request):
    ocrs = OCR.objects.filter(published=True)

    if request.method == 'GET':
        ocrs_serializer = OCRSerializer(ocrs, many=True)
        return Response(ocrs_serializer.data)
