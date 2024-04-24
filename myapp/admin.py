# admin.py

from django.contrib import admin
from .models import SongFeature, GenreInfo
from django.utils.html import format_html
import json


class SongFeatureAdmin(admin.ModelAdmin):
    list_display = ('file_path', 'genre', 'scene', 'year', 'tempo',
                    'average_spectral_centroid', 'average_spectral_rolloff',
                    'formatted_average_spectral_contrast', 'formatted_mfccs_mean',
                    'average_chroma_stft', 'average_rms_energy', 'formatted_vggish_embeddings')

    search_fields = ['file_path', 'genre']
    list_filter = ('genre', 'tempo')

    def formatted_average_spectral_contrast(self, obj):
        return self._format_list_field(obj.average_spectral_contrast)

    formatted_average_spectral_contrast.short_description = 'Average Spectral Contrast (Preview)'

    def formatted_mfccs_mean(self, obj):
        return self._format_list_field(obj.mfccs_mean)

    formatted_mfccs_mean.short_description = 'MFCCs Mean (Preview)'

    def formatted_vggish_embeddings(self, obj):
        # Adjust formatting as needed, depending on how VGGish embeddings are stored
        return self._format_list_field(obj.vggish_embeddings)

    formatted_vggish_embeddings.short_description = 'VGGish Embeddings (Preview)'

    def _format_list_field(self, list_field):
        if list_field:
            list_data = json.loads(list_field)[:5]  # Convert string to list and take first 5 elements
            formatted_list = ', '.join([str(item) for item in list_data]) + '...'
            return format_html('<span title="{}">{}</span>', list_field, formatted_list)
        return ''

admin.site.register(SongFeature, SongFeatureAdmin)
class GenreInfoAdmin(admin.ModelAdmin):
    def parent_genres_list(self, obj):
        # Fetch all parent genres and return their names joined by commas
        parents = obj.parent_genres.all()
        return ", ".join([parent.genre for parent in parents])

    parent_genres_list.short_description = 'Parent Genres'

    def child_genres_list(self, obj):
        # Fetch all child genres and return their names joined by commas
        children = obj.derived_genres.all()
        return ", ".join([child.genre for child in children])

    child_genres_list.short_description = 'Derived Genres (Children)'

    def formatted_aka(self, obj):
        try:
            # Attempt to load the JSON data
            aka_list = json.loads(obj.aka)
            return ", ".join(aka_list)
        except json.JSONDecodeError:
            # Return a default value or the raw string if JSON decoding fails
            return obj.aka or "N/A"  # You can replace "N/A" with any placeholder text you prefer

    formatted_aka.short_description = 'AKA (Aliases)'

    def formation_period(self, obj):
        return f"{obj.formation_start_year} - {obj.formation_end_year}" if obj.formation_start_year and obj.formation_end_year else "N/A"

    formation_period.short_description = 'Formation Period'

    def active_period(self, obj):
        return f"{obj.active_start_year} - {obj.active_end_year}" if obj.active_start_year and obj.active_end_year else "N/A"

    active_period.short_description = 'Active Period'


    list_display = [
        'genre', 'scene', 'parent_genres_list', 'formatted_aka',
        'child_genres_list', 'formation_period', 'active_period'
    ]
    search_fields = ['genre', 'scene']
    list_filter = ['scene']


# Register GenreInfo with the custom admin class
admin.site.register(GenreInfo, GenreInfoAdmin)