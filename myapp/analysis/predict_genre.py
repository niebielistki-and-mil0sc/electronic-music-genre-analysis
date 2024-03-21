# predict_genre.py
import os
import django
import numpy as np
from joblib import load

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from genre_utils import find_relevant_genres
from analiza import analyze_mp3

MODEL_PATH = 'genre_classifier.joblib'
SCALER_PATH = 'scaler.joblib'
LABEL_ENCODER_PATH = 'label_encoder.joblib'

def adjust_probabilities(probabilities, label_encoder, relevant_genres):
    adjusted_probs = {}
    for genre, prob in probabilities.items():
        # Give more weight to historically relevant genres
        if genre in relevant_genres:
            adjusted_probs[genre] = prob * 1.5  # Example weight multiplier for relevant genres
        else:
            adjusted_probs[genre] = prob * 0.5  # Example weight multiplier for non-relevant genres

    # Normalize the probabilities to sum to 1
    total_prob = sum(adjusted_probs.values())
    normalized_probs = {genre: prob / total_prob for genre, prob in adjusted_probs.items()}
    return normalized_probs

def predict_genre(file_path):
    # Load the model, scaler, and label encoder
    model = load(MODEL_PATH)
    scaler = load(SCALER_PATH)
    label_encoder = load(LABEL_ENCODER_PATH)

    # Analyze the MP3 to get its features
    feature_dict = analyze_mp3(file_path)

    # Extract the year from the filename
    filename = os.path.basename(file_path)
    year = int(filename.split(' - ')[0])
    relevant_genres = find_relevant_genres(year)

    # Ensure this matches the order and selection of features used in your ml_preparation.py
    features = np.array([
        feature_dict['tempo'],
        feature_dict['average_spectral_centroid'],
        feature_dict['average_spectral_rolloff'],
        np.mean(feature_dict['average_spectral_contrast']),
        *feature_dict['mfccs_mean'],
        np.mean(feature_dict['average_chroma_stft']),
        np.mean(feature_dict['average_rms_energy']),
    ]).reshape(1, -1)  # Reshape for a single sample

    # Scale the features
    features_scaled = scaler.transform(features)

    # Predict the genre
    probabilities = model.predict_proba(features_scaled)[0]
    genre_probabilities = {label_encoder.classes_[i]: prob for i, prob in enumerate(probabilities)}

    # Adjust the probabilities based on genre relevance
    adjusted_probs = adjust_probabilities(genre_probabilities, label_encoder, relevant_genres)

    # Print the adjusted probabilities
    print("Adjusted predicted genre probabilities:")
    for genre, probability in sorted(adjusted_probs.items(), key=lambda x: x[1], reverse=True):
        print(f"{genre}: {probability * 100:.2f}%")

if __name__ == "__main__":
    new_song_path = '/Users/wiktoria/PycharmProjects/music-project/myapp/analysis/ishkur/Funk/1972 - Funk - Urban - Ohio Players - Funky Worm.mp3'  # Change to the path of the song you want to analyze
    predict_genre(new_song_path)
