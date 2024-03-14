from django.contrib import admin
from .models import SongFeature
from django.utils.html import format_html


class SongFeatureAdmin(admin.ModelAdmin):
    # This list_display allows you to choose which fields to display in the admin list view.
    list_display = ('file_path', 'genre', 'tempo', 'average_spectral_centroid', 'average_spectral_rolloff',
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
