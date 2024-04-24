import os
import django
import torch
import numpy as np
from joblib import load
import json
from torch.nn.functional import softmax
from myapp.analysis.nn_models import CNNModel
from myapp.analysis.analiza import analyze_mp3, get_vggish_embeddings  # Assuming get_vggish_embeddings is properly implemented here

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Define paths for the model, scaler, label encoder, and model config
BASE_MODEL_PATH = '/Users/wiktoria/PycharmProjects/music-project/myapp/analysis/models/trained_model.pth'
BASE_SCALER_PATH = '/Users/wiktoria/PycharmProjects/music-project/myapp/analysis/scalers/scaler.joblib'
LABEL_ENCODER_PATH = '/Users/wiktoria/PycharmProjects/music-project/myapp/analysis/label_encoders/label_encoder.joblib'
MODEL_CONFIG_PATH = '/Users/wiktoria/PycharmProjects/music-project/myapp/analysis/model_config.json'


def load_model_config(config_path=MODEL_CONFIG_PATH):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config['input_length'], config['num_classes']

def predict_genre(file_path):
    try:
        input_length, num_classes = load_model_config()

        # Load the scaler and label encoder
        scaler = load(BASE_SCALER_PATH)
        label_encoder = load(LABEL_ENCODER_PATH)

        # Initialize the model with the loaded configurations
        model = CNNModel(input_channels=1, input_length=input_length, num_classes=num_classes)
        model.load_state_dict(torch.load(BASE_MODEL_PATH))
        model.eval()

        # Extract features and VGGish embeddings using analyze_mp3 and get_vggish_embeddings functions
        feature_dict = analyze_mp3(file_path)
        vggish_features = get_vggish_embeddings(file_path)  # This should return the flattened VGGish embeddings as a list
        if feature_dict is None or vggish_features is None:
            raise ValueError("Failed to extract features from the audio file.")

        # Prepare the full feature array for prediction, including VGGish features
        features = np.concatenate([
            np.array([
                feature_dict['tempo'],
                feature_dict['average_spectral_centroid'],
                feature_dict['average_spectral_rolloff'],
                np.mean(feature_dict['average_spectral_contrast']),
                *feature_dict['mfccs_mean'],
                feature_dict['average_chroma_stft'],
                feature_dict['average_rms_energy']
            ]),
            vggish_features  # Add VGGish embeddings directly
        ]).reshape(1, -1)  # Reshape for a single sample

        # Scale features
        features_scaled = scaler.transform(features)
        features_scaled = torch.tensor(features_scaled, dtype=torch.float32).unsqueeze(1)  # Add channel dimension for CNN input

        # Make the prediction
        with torch.no_grad():
            logits = model(features_scaled)
            probabilities = softmax(logits, dim=1)
            genre_probabilities = probabilities.numpy()[0]  # Convert to numpy array and get the first (and only) item

        # Display the probabilities
        genres = label_encoder.classes_
        for genre, probability in zip(genres, genre_probabilities):
            return {genre: f"{probability * 100:.2f}%" for genre, probability in zip(genres, genre_probabilities)}

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
