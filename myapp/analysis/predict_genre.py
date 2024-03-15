# predict_genre.py
from joblib import load
import numpy as np

# Adjust the import path as needed.
from analiza import analyze_mp3

MODEL_PATH = 'genre_classifier.joblib'
SCALER_PATH = 'scaler.joblib'
LABEL_ENCODER_PATH = 'label_encoder.joblib'

def predict_genre(file_path):
    # Load the model, scaler, and label encoder
    model = load(MODEL_PATH)
    scaler = load(SCALER_PATH)
    label_encoder = load(LABEL_ENCODER_PATH)

    # Analyze the MP3 to get its features
    feature_dict = analyze_mp3(file_path)

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

    # Print the probabilities
    print("Predicted genre probabilities:")
    for genre, probability in sorted(genre_probabilities.items(), key=lambda x: x[1], reverse=True):
        print(f"{genre}: {probability * 100:.2f}%")

if __name__ == "__main__":
    new_song_path = '/Users/milosz/Desktop/ishkur/Funk/1981 - Funk - Rick James - Give It To Me Baby.mp3'  # Change to the path of the song you want to analyze
    predict_genre(new_song_path)
