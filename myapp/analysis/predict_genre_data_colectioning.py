import os
import django
import torch
import numpy as np
from joblib import load
import json
from torch.nn.functional import softmax
from glob import glob
import csv
from myapp.analysis.nn_models import CNNModel
from myapp.analysis.analiza import analyze_mp3

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Define paths for the model, scaler, label encoder, and model config
BASE_MODEL_PATH = '/Users/milosz/python/pyCharm/music-project/myapp/analysis/models/trained_model.pth'
BASE_SCALER_PATH = '/Users/milosz/python/pyCharm/music-project/myapp/analysis/scalers/scaler.joblib'
LABEL_ENCODER_PATH = '/Users/milosz/python/pyCharm/music-project/myapp/analysis/label_encoders/label_encoder.joblib'
MODEL_CONFIG_PATH = '/Users/milosz/python/pyCharm/music-project/myapp/analysis/model_config.json'

# Load model config
def load_model_config(config_path=MODEL_CONFIG_PATH):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config['input_length'], config['num_classes']

# Predict genre for a single file
def predict_genre(file_path):
    try:
        input_length, num_classes = load_model_config()
        scaler = load(BASE_SCALER_PATH)
        label_encoder = load(LABEL_ENCODER_PATH)
        model = CNNModel(input_channels=1, input_length=input_length, num_classes=num_classes)
        model.load_state_dict(torch.load(BASE_MODEL_PATH))
        model.eval()
        feature_dict = analyze_mp3(file_path)
        if feature_dict is None:
            raise ValueError("Failed to extract features from the audio file.")
        features = np.array([
            feature_dict['tempo'],
            feature_dict['average_spectral_centroid'],
            feature_dict['average_spectral_rolloff'],
            np.mean(feature_dict['average_spectral_contrast']),
            *feature_dict['mfccs_mean'],
            feature_dict['average_chroma_stft'],
            feature_dict['average_rms_energy'],
        ]).reshape(1, -1)
        features_scaled = scaler.transform(features)
        features_scaled = torch.tensor(features_scaled, dtype=torch.float32).unsqueeze(1)
        with torch.no_grad():
            logits = model(features_scaled)
            probabilities = softmax(logits, dim=1)
            genre_probabilities = probabilities.numpy()[0]
        genres = label_encoder.classes_
        return {
            file_path: {genre: f"{probability * 100:.2f}%" for genre, probability in zip(genres, genre_probabilities)}
        }
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return {file_path: "FileNotFoundError"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {file_path: "Error"}

# Process directory and predict genres
def process_directory(directory_path):
    predictions = {}
    for file_path in glob(os.path.join(directory_path, '*.mp3')):
        prediction = predict_genre(file_path)
        predictions.update(prediction)
    return predictions

# Main execution
if __name__ == "__main__":
    funk_predictions = process_directory('/Users/milosz/Desktop/test/funk')
    italo_disco_predictions = process_directory('/Users/milosz/Desktop/test/italo-disco')
    all_predictions = {**funk_predictions, **italo_disco_predictions}

    # Save predictions to CSV
    csv_file_path = '/Users/milosz/Desktop/test/predictions5.csv'
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['File Path', 'Genre', 'Probability'])
        for file_path, genres_prob in all_predictions.items():
            if isinstance(genres_prob, str):  # Handling errors
                writer.writerow([file_path, 'Error', genres_prob])
            else:
                for genre, prob in genres_prob.items():
                    writer.writerow([file_path, genre, prob])

    print(f"Predictions saved to {csv_file_path}")
