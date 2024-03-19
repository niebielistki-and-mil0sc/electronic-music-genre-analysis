# genre_utils.py
import os
import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from myapp.models import GenreRelationship

def find_relevant_genres(year):
    relationships = GenreRelationship.objects.filter(
        start_year__lte=year,
        end_year__gte=year
    )
    return [rel.target for rel in relationships]