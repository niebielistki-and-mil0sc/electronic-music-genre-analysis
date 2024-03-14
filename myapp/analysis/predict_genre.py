# predict_genre.py
from joblib import load
import numpy as np

# Make sure to define or adjust analyze_mp3_for_prediction appropriately
from analiza import analyze_mp3

MODEL_PATH = 'genre_classifier.joblib'
SCALER_PATH = 'scaler.joblib'

def predict_genre(file_path):
    model = load(MODEL_PATH)
    scaler = load(SCALER_PATH)

    feature_dict = analyze_mp3(file_path)

    # Ensure this matches the order and selection of features used in your ml_preparation.py
    features = [
        feature_dict['tempo'],
        feature_dict['average_spectral_centroid'],
        feature_dict['average_spectral_rolloff'],
        np.mean(np.array(feature_dict['average_spectral_contrast'])),
        *feature_dict['mfccs_mean'],
        feature_dict['average_chroma_stft'],
        feature_dict['average_rms_energy'],
    ]

    features_scaled = scaler.transform([features])

    prediction = model.predict(features_scaled)
    print("Predicted genre index:", prediction[0])

if __name__ == "__main__":
    new_song_path = '/Users/milosz/Downloads/Parliament - Flashlight (HQ).mp3'
    predict_genre(new_song_path)



