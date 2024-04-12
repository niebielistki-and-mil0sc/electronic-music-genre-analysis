import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Import the GenreInfo model
from myapp.models import GenreInfo

def print_and_count_genres():
    # Query to get all genre names
    genres = GenreInfo.objects.all().values_list('genre', flat=True)
    total_genres = len(genres)  # Count the total number of genres

    print(f"Total genres in the database: {total_genres}\n")

    # Prepare the genre list for display
    genres_list = ", ".join(f"'{genre}'" for genre in genres)
    print(f"List of genres: [{genres_list}]")

if __name__ == '__main__':
    print_and_count_genres()
