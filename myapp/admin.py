# admin.py

from django.contrib import admin
from .models import SongFeature, GenreRelationship, GenreInfo
from django.utils.html import format_html
import json


class SongFeatureAdmin(admin.ModelAdmin):
    # This list_display allows you to choose which fields to display in the admin list view.
    list_display = ('file_path', 'genre', 'scene', 'tempo', 'average_spectral_centroid', 'average_spectral_rolloff',
                    'formatted_average_spectral_contrast', 'formatted_mfccs_mean', 'average_chroma_stft',
                    'average_rms_energy')

    # Adding a search functionality to search through the file paths and genres.
    search_fields = ['file_path', 'genre']

    # Enable filtering by genre and tempo, which could be useful for quickly finding songs of a certain type.
    list_filter = ('genre', 'tempo')

    # Custom methods to format the serialized list fields for better readability in the list view.
    # These methods return the first few elements of the list for a quick preview.
    def formatted_average_spectral_contrast(self, obj):
        return self._format_list_field(obj.average_spectral_contrast)

    formatted_average_spectral_contrast.short_description = 'Average Spectral Contrast (Preview)'

    def formatted_mfccs_mean(self, obj):
        return self._format_list_field(obj.mfccs_mean)

    formatted_mfccs_mean.short_description = 'MFCCs Mean (Preview)'

    # Utility method to format list fields.
    def _format_list_field(self, list_field):
        if list_field:
            list_data = list_field.strip('[]').split(',')[
                        :5]  # Assuming it's stored as a string representation of a list.
            formatted_list = ', '.join(list_data) + '...'
            return format_html('<span title="{}">{}</span>', list_field, formatted_list)
        return ''

    # This ensures the custom formatting methods are safe from auto-escaping
    formatted_average_spectral_contrast.allow_tags = True
    formatted_mfccs_mean.allow_tags = True


# Register your models here, linking them with the custom admin classes.
admin.site.register(SongFeature, SongFeatureAdmin)

# Include GenreRelationship in your admin
class GenreRelationshipAdmin(admin.ModelAdmin):
    list_display = ('source', 'target', 'start_year', 'end_year')

admin.site.register(GenreRelationship, GenreRelationshipAdmin)


class GenreInfoAdmin(admin.ModelAdmin):
    def parent_genres_list(self, obj):
        # Fetch all parent genres and return their names joined by commas
        parents = obj.parent_genres.all()
        return ", ".join([parent.genre for parent in parents])

    parent_genres_list.short_description = 'Parent Genres'

    list_display = ['genre', 'scene', 'parent_genres_list', 'formatted_aka', 'child_genres_list']
    search_fields = ['genre', 'scene']
    list_filter = ['scene']

    def formatted_aka(self, obj):
        try:
            # Attempt to load the JSON data
            aka_list = json.loads(obj.aka)
            return ", ".join(aka_list)
        except json.JSONDecodeError:
            # Return a default value or the raw string if JSON decoding fails
            return obj.aka or "N/A"  # You can replace "N/A" with any placeholder text you prefer

    formatted_aka.short_description = 'AKA (Aliases)'

    def child_genres_list(self, obj):
        # Fetch all child genres and return their names joined by commas
        children = obj.derived_genres.all()
        return ", ".join([child.genre for child in children])

    child_genres_list.short_description = 'Derived Genres (Children)'

# Register GenreInfo with the custom admin class
admin.site.register(GenreInfo, GenreInfoAdmin)