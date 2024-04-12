import os
import django
import numpy as np
import librosa
import json
from torchvggish import vggish, vggish_input

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from myapp.models import SongFeature  # Ensure the correct import path to your SongFeature model

# Initialize the VGGish model
embedding_model = vggish()
embedding_model.eval()

def analyze_mp3(file_path):
    """
    Analyzes an MP3 file with Librosa and returns various audio features.
    """
    print(f"Analyzing {file_path} with Librosa...")
    y, sr = librosa.load(file_path, sr=None)
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)

    features = {
        'tempo': tempo,
        'average_spectral_centroid': np.mean(spectral_centroids),
        'average_spectral_rolloff': np.mean(spectral_rolloff),
        'average_spectral_contrast': np.mean(spectral_contrast, axis=1).tolist(),
        'mfccs_mean': np.mean(mfccs, axis=1).tolist(),
        'average_chroma_stft': np.mean(chroma_stft),
        'average_rms_energy': np.mean(rms)
    }
    print(f"Features extracted for {file_path}: {features}")
    return features


def get_vggish_embeddings(file_path, desired_length=13000):
    """
    Extracts embeddings from an audio file using the VGGish model, ensuring they have a uniform length.
    :param file_path: Path to the audio file.
    :param desired_length: The uniform length for the embeddings.
    :return: A list of VGGish embeddings with the specified uniform length.
    """
    print(f"Extracting VGGish embeddings for {file_path}...")
    examples = vggish_input.wavfile_to_examples(file_path)
    embeddings = embedding_model.forward(examples)
    vggish_features = embeddings.detach().numpy().flatten()

    # Ensure the embeddings have the uniform desired_length
    if len(vggish_features) > desired_length:
        vggish_features = vggish_features[:desired_length]  # Truncate
    elif len(vggish_features) < desired_length:
        # Pad with zeros
        vggish_features = np.pad(vggish_features, (0, desired_length - len(vggish_features)), mode='constant',
                                 constant_values=0)

    print(f"VGGish embeddings extracted for {file_path}, adjusted to uniform length.")
    return list(map(float, vggish_features))


def process_and_store_data(base_dir):
    """
    Processes MP3 files in the given directory and stores extracted features in the database.
    """
    print(f"Scanning directory: {base_dir}")
    for filename in os.listdir(base_dir):
        if filename.lower().endswith('.mp3'):
            file_path = os.path.join(base_dir, filename)
            print(f"Processing file: {file_path}")
            try:
                parts = filename.replace('.mp3', '').split(' - ')
                if len(parts) >= 3:
                    year = int(parts[0])
                    genre = parts[1]
                    scene = ' '.join(parts[2:-1])
                else:
                    print(f"Filename format does not match expected pattern: {filename}")
                    continue  # Skip this file

                librosa_features = analyze_mp3(file_path)
                vggish_features = get_vggish_embeddings(file_path)

                song_feature_instance = SongFeature.objects.create(
                    file_path=file_path,
                    genre=genre,
                    scene=scene,
                    year=year,
                    tempo=librosa_features.get('tempo', 0),
                    average_spectral_centroid=librosa_features.get('average_spectral_centroid', 0),
                    average_spectral_rolloff=librosa_features.get('average_spectral_rolloff', 0),
                    average_spectral_contrast=json.dumps(librosa_features.get('average_spectral_contrast', [])),
                    mfccs_mean=json.dumps(librosa_features.get('mfccs_mean', [])),
                    average_chroma_stft=librosa_features.get('average_chroma_stft', 0),
                    average_rms_energy=librosa_features.get('average_rms_energy', 0),
                    vggish_embeddings=json.dumps(vggish_features)  # Corrected field name
                )

                print(f"Successfully saved data for {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")


if __name__ == "__main__":
    base_dir = '/Users/milosz/Desktop/ishkur/'  # Set to your top-level directory

    # Iterate through each item in the base directory
    for item in os.listdir(base_dir):
        # Construct the full path of the item
        item_path = os.path.join(base_dir, item)

        # Check if the item is a directory (and not a file like 'ishkur-songs.csv')
        if os.path.isdir(item_path):
            print(f"Processing directory: {item_path}")
            process_and_store_data(item_path)
        else:
            print(f"Skipping non-directory item: {item_path}")