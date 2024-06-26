# models.py
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

class SongFeature(models.Model):
    file_path = models.CharField(max_length=1024)
    genre = models.CharField(max_length=255)
    scene = models.CharField(max_length=255, default='Unknown')
    year = models.IntegerField(null=True, blank=True)
    tempo = models.FloatField()
    average_spectral_centroid = models.FloatField()
    average_spectral_rolloff = models.FloatField()
    average_spectral_contrast = models.TextField()  # This will be a list converted to string
    mfccs_mean = models.TextField()  # Likewise, a list converted to string
    average_chroma_stft = models.FloatField()
    average_rms_energy = models.FloatField()
    vggish_embeddings = models.TextField(default=DjangoJSONEncoder().encode([]))  # For VGGish features

    def __str__(self):
        return self.file_path

    class Meta:
        verbose_name = "Song Feature"
        verbose_name_plural = "Song Features"

class GenreInfo(models.Model):
    slug = models.CharField(max_length=255, unique=True, help_text="The genre's slug, a URL-friendly version of its name.")
    genre = models.CharField(max_length=255, help_text="The name of the genre.")
    scene = models.CharField(max_length=255, blank=True, null=True, help_text="The scene from which this genre originated.")
    emerged = models.CharField(max_length=255, blank=True, null=True, help_text="The approximate period or decade when this genre first emerged.")
    aka = models.TextField(default=DjangoJSONEncoder().encode([]), help_text="Other names or aliases for the genre.")
    parent_genres = models.ManyToManyField('self', symmetrical=False, related_name='derived_genres', blank=True, help_text="The parent genre from which this genre arose.")
    duration_start = models.IntegerField(blank=True, null=True, help_text="The year when the genre's distinct period started.")
    duration_end = models.IntegerField(blank=True, null=True, help_text="The year when the genre's distinct period ended or the current year if it's ongoing.")
    formation_start_year = models.IntegerField(null=True, blank=True, help_text="The year when the genre began forming.")
    formation_end_year = models.IntegerField(null=True, blank=True, help_text="The year when the genre's formation was essentially complete.")
    active_start_year = models.IntegerField(null=True, blank=True, help_text="The year when the genre became distinctively active.")
    active_end_year = models.IntegerField(null=True, blank=True, help_text="The year when the genre's initial active period ended or the current year if it's ongoing.")

    def get_child_genres(self):
        return self.derived_genres.all()

    def __str__(self):
        return self.genre

    class Meta:
        verbose_name = "Genre Info"
        verbose_name_plural = "Genre Info"
