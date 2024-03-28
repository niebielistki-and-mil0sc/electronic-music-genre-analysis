from django.urls import path
from .views import GenrePredictionAPI

urlpatterns = [
    path('predict-genre/', GenrePredictionAPI.as_view(), name='predict_genre'),
]
