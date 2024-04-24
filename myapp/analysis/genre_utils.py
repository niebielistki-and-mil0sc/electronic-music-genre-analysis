# genre_utils.py

import os
import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from myapp.models import GenreInfo

def find_relevant_genres(year):
    """
    Finds genres that are relevant for a given year based on their active period.
    """
    relevant_genres = GenreInfo.objects.filter(
        Q(active_start_year__lte=year, active_end_year__gte=year) |
        Q(formation_start_year__lte=year, formation_end_year__gte=year)
    )
    return [genre.genre for genre in relevant_genres]

# Example usage
if __name__ == "__main__":
    year = 1990
    print(f"Genres relevant in {year}: {find_relevant_genres(year)}")
