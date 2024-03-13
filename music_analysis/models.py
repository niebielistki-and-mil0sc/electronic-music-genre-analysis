# models.py
from django.db import models

class SongFeature(models.Model):
    file_path = models.CharField(max_length=1024)
    genre = models.CharField(max_length=255)
    tempo = models.FloatField()
    average_spectral_centroid = models.FloatField()
    average_spectral_rolloff = models.FloatField()
    average_spectral_contrast = models.TextField()  # This will be a list converted to string
    mfccs_mean = models.TextField()  # Likewise, a list converted to string
    average_chroma_stft = models.FloatField()
    average_rms_energy = models.FloatField()

    def __str__(self):
        return self.file_path
