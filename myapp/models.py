# models.py
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

class SongFeature(models.Model):
    file_path = models.CharField(max_length=1024)
    genre = models.CharField(max_length=255)
    scene = models.CharField(max_length=255, default='Unknown')
    tempo = models.FloatField()
    average_spectral_centroid = models.FloatField()
    average_spectral_rolloff = models.FloatField()
    average_spectral_contrast = models.TextField()  # This will be a list converted to string
    mfccs_mean = models.TextField()  # Likewise, a list converted to string
    average_chroma_stft = models.FloatField()
    average_rms_energy = models.FloatField()
    # New field to store relevant genres as a JSON string
    relevant_genres = models.TextField(default=DjangoJSONEncoder().encode([]))

    def __str__(self):
        return self.file_path

class GenreRelationship(models.Model):
    source = models.CharField(max_length=255)  # Parent genre/subgenre
    target = models.CharField(max_length=255)  # Child genre/subgenre that evolved from source
    start_year = models.IntegerField()         # Year when the relationship started
    end_year = models.IntegerField()           # Year when the relationship ended (or current year if it's ongoing)
