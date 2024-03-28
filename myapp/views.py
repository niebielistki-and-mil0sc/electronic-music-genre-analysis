# views.py
import os
import django
from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers import FileUploadSerializer
from myapp.analysis.predict_genre import predict_genre

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


class GenrePredictionAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            file_path = default_storage.save(file.name, file)
            full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            prediction = predict_genre(full_file_path)
            return Response(prediction, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        return Response({"message": "GET request received, but this endpoint expects a POST request with a file."})
