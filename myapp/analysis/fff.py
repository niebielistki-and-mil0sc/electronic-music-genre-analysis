import json
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from myapp.models import SongFeature

def print_vggish_lengths():
    all_songs = SongFeature.objects.all()

    for song in all_songs:
        vggish_embeddings = json.loads(song.vggish_embeddings)
        print(f"Song ID {song.id} VGGish Embeddings Length: {len(vggish_embeddings)}")

if __name__ == "__main__":
    print_vggish_lengths()
