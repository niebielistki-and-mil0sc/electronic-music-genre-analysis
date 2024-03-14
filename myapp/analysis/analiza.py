# analiza.py
import os
import django
import numpy as np
import librosa
import json

# Initialize Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from myapp.models import SongFeature


def analyze_mp3(file_path):
    """
    Analyzes an MP3 file and returns various audio features.
    """
    y, sr = librosa.load(file_path, sr=None)

    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfccs_mean = np.mean(mfccs, axis=1)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)

    return {
        'file_path': file_path,
        'tempo': tempo,
        'average_spectral_centroid': np.mean(spectral_centroids),
        'average_spectral_rolloff': np.mean(spectral_rolloff),
        'average_spectral_contrast': np.mean(spectral_contrast, axis=1).tolist(),
        'mfccs_mean': mfccs_mean.tolist(),
        'average_chroma_stft': np.mean(chroma_stft),
        'average_rms_energy': np.mean(rms)
    }


def process_and_store_data(base_dir):
    """
    Processes MP3 files in the given directory and stores extracted features in the database.
    """
    for genre in os.listdir(base_dir):
        genre_dir = os.path.join(base_dir, genre)
        if os.path.isdir(genre_dir):
            for filename in os.listdir(genre_dir):
                if filename.endswith('.mp3'):
                    file_path = os.path.join(genre_dir, filename)
                    try:
                        features = analyze_mp3(file_path)
                        SongFeature.objects.create(
                            file_path=features['file_path'],
                            genre=genre,
                            tempo=features['tempo'],
                            average_spectral_centroid=features['average_spectral_centroid'],
                            average_spectral_rolloff=features['average_spectral_rolloff'],
                            average_spectral_contrast=json.dumps(features['average_spectral_contrast']),
                            mfccs_mean=json.dumps(features['mfccs_mean']),
                            average_chroma_stft=features['average_chroma_stft'],
                            average_rms_energy=features['average_rms_energy']
                        )
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")


# Replace 'your_project_name.settings' with the path to your Django project's settings module Replace
# 'your_app_name.models' and 'SongFeature' with the actual app name and model class where you intend to store the
# features

if __name__ == "__main__":
    base_dir = '/Users/wiktoria/PycharmProjects/music-project/myapp/analysis/ishkur/Funk'  # Update this path to your dataset directory
    process_and_store_data(base_dir)
