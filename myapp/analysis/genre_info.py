#genre_info.py
import csv
import django
import os
import json


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from myapp.models import GenreInfo, GenreRelationship

# Clear existing relationships
for genre_info in GenreInfo.objects.all():
    genre_info.parent_genres.clear()


# Function to load genres from v3_genres.csv
def load_genres_from_csv(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            aka_list = row['aka'].split(', ')  # Assuming aliases are comma-separated in your CSV
            genre, created = GenreInfo.objects.get_or_create(slug=row['slug'], defaults={
                'genre': row['genre'],
                'scene': row['scene'],
                'aka': json.dumps(aka_list)  # Store aliases as a JSON-encoded list
            })


def update_genre_relationships_and_duration(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Get or create the child genre
                child_genre, _ = GenreInfo.objects.get_or_create(slug=row['target'], defaults={'genre': row['target']})

                # Update duration based on the dataset
                child_genre.duration_start = int(row['start'])
                child_genre.duration_end = int(row['end'])
                child_genre.save()  # Save the child genre to ensure it exists for ManyToMany relations

                # Find and add parent genres, avoiding adding itself as a parent
                parent_genre_slugs = [slug.strip() for slug in
                                      row['source'].split(',')]  # Splitting and stripping to avoid whitespace issues
                for slug in parent_genre_slugs:
                    if slug != row['target']:  # Prevent a genre from being its own parent
                        parent_genre, _ = GenreInfo.objects.get_or_create(slug=slug, defaults={'genre': slug})
                        child_genre.parent_genres.add(parent_genre)


            except GenreInfo.DoesNotExist:
                print(f"Genre not found for slug: {row['source']} or {row['target']}")


if __name__ == "__main__":
    load_genres_from_csv('/Users/wiktoria/PycharmProjects/music-project/myapp/analysis/ishkur/v3_genres.csv')
    update_genre_relationships_and_duration('/Users/wiktoria/PycharmProjects/music-project/myapp/analysis/ishkur/ishkur-guide-dataset.csv')
