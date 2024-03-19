# genre_relationships.py

import os
import django
import csv

# Ensure the correct settings module is set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from myapp.models import GenreRelationship

def import_genre_relationships(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            GenreRelationship.objects.create(
                source=row['source'],
                target=row['target'],
                start_year=int(row['start']),
                end_year=int(row['end'])
            )


if __name__ == "__main__":
    # Replace with the actual path to your CSV file
    csv_file_path = '/Users/wiktoria/PycharmProjects/music-project/myapp/analysis/ishkur/ishkur-guide-dataset.csv'
    import_genre_relationships(csv_file_path)


