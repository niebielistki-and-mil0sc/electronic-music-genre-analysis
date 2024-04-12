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
from tempfile import NamedTemporaryFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()



class GenrePredictionAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            with NamedTemporaryFile(delete=True) as tmp:
                for chunk in file.chunks():
                    tmp.write(chunk)
                tmp.flush()
                prediction = predict_genre(tmp.name)
            return Response(prediction, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
