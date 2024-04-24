import os
import django

# Setting up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Update 'your_project.settings' accordingly
django.setup()

from myapp.models import SongFeature  # Update 'your_app.models' to the correct path


def delete_entries_without_year():
    """
    Deletes all entries in the SongFeature model where the year is None.
    """
    # Filter for entries without a year
    entries_without_year = SongFeature.objects.filter(year__isnull=True)

    count = entries_without_year.count()  # For reporting how many entries will be deleted

    # Delete the filtered entries
    entries_without_year.delete()

    print(f"Deleted {count} entries from SongFeature where the year was None.")


if __name__ == "__main__":
    delete_entries_without_year()
