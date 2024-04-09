from django.core.management.base import BaseCommand
from myapp.models import SongFeature

class Command(BaseCommand):
    help = 'Deletes all entries in the SongFeature model'

    def handle(self, *args, **kwargs):
        # Confirm before deleting
        if input("Are you sure you want to delete all SongFeature entries? (yes/no): ") == 'yes':
            count = SongFeature.objects.all().delete()[0]
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} SongFeature entries.'))
        else:
            self.stdout.write(self.style.WARNING('Operation cancelled.'))
