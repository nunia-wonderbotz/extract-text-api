from rest_framework import serializers
from OCR.models import OCR

class OCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCR
        fields = "__all__"