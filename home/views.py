from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PDFSerializer
from django.conf import settings
from pdfsummarizer.celery import summarize_pdf

class PDFSummarizerAPI(APIView):
    def get(self, request):
        return Response({
            "message": "Welcome to pdf summarizer API!!"
        })
    
    def post(self, request):
        serializer = PDFSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            actual_path = serializer.instance.pdf_file.path
            # print(actual_path)

            # Calling by celery
            data = summarize_pdf.delay(actual_path)
            # print(data)
            return Response({
                "message": "PDF file uploaded successfully!",
                "task_id": str(data.id)
            }, status=201)
        return Response(serializer.errors, status=400)