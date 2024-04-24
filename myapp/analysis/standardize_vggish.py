import os
import django
import numpy as np
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from myapp.models import SongFeature  # Adjust 'myapp' to the actual app name



def standardize_embeddings(embeddings, target_length):
    """
    Standardize the length of VGGish embeddings to a target length.
    If an embedding is shorter than the target, it will be padded with zeros.
    If it's longer, it will be truncated to fit the target length.

    Parameters:
    - embeddings: The original embeddings as a numpy array.
    - target_length: The desired length of the embeddings.

    Returns:
    - A numpy array of the standardized embeddings.
    """
    current_length = len(embeddings)
    if current_length < target_length:
        # Pad with zeros
        padding = np.zeros(target_length - current_length)
        standardized_embeddings = np.concatenate((embeddings, padding))
    elif current_length > target_length:
        # Truncate
        standardized_embeddings = embeddings[:target_length]
    else:
        # No change needed
        standardized_embeddings = embeddings
    return standardized_embeddings


def load_features_and_labels():
    all_songs = SongFeature.objects.all()
    features = []
    labels = []
    target_embedding_length = 128

    for song in all_songs:
        try:
            spectral_contrast = np.mean(np.array(json.loads(song.average_spectral_contrast), dtype=float))
            mfccs_mean = np.array(json.loads(song.mfccs_mean), dtype=float)
            raw_vggish_embeddings = np.array(json.loads(song.vggish_embeddings), dtype=float)
            vggish_embeddings = standardize_embeddings(raw_vggish_embeddings, target_embedding_length)

            song_features = [song.tempo, song.average_spectral_centroid, ..., *vggish_embeddings]

            # Debug: Print the length of the combined feature vector
            print(f"Length of combined feature vector for {song.file_path}: {len(song_features)}")

            features.append(song_features)
            labels.append(song.genre)
        except Exception as e:
            print(f"Error processing song {song.file_path}: {e}")

    if not features:
        print("No data found, returning None.")
        return None, None

    return np.array(features, dtype=float), np.array(labels)

# Ensure the rest of your script properly calls load_features_and_labels()
