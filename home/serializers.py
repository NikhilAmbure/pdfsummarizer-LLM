from rest_framework import serializers
from .models import *


class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = pdf_upload
        fields = '__all__'