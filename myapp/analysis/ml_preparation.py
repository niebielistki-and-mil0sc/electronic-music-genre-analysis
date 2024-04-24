# ml_preparation
import json
import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import django
from django.apps import apps
from joblib import dump
from myapp.analysis.nn_models import CNNModel

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Replace 'your_app' and 'SongFeature' with your actual app and model name
SongFeature = apps.get_model('myapp', 'SongFeature')


def train_and_save_models():
    # Paths setup
    base_path = os.path.dirname(__file__)  # Adjust as needed for your project structure
    models_path = os.path.join(base_path, 'models')
    scalers_path = os.path.join(base_path, 'scalers')
    label_encoders_path = os.path.join(base_path, 'label_encoders')
    os.makedirs(models_path, exist_ok=True)
    os.makedirs(scalers_path, exist_ok=True)
    os.makedirs(label_encoders_path, exist_ok=True)

    # Load and preprocess data
    features, labels = load_features_and_labels()
    # Note the added scaler and label_encoder in the return statement below
    X_train, X_test, y_train, y_test, scaler, label_encoder = preprocess_data(features, labels)
    X_train = X_train.reshape((X_train.shape[0], 1, -1))
    X_test = X_test.reshape((X_test.shape[0], 1, -1))

    # Prepare DataLoader
    train_loader, test_loader = create_dataloaders(X_train, X_test, y_train, y_test)

    # Initialize and train model
    num_classes = len(np.unique(y_train))
    model = CNNModel(input_channels=1, input_length=X_train.shape[2], num_classes=num_classes)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    train_model(model, criterion, optimizer, train_loader, test_loader, epochs=10)

    # Save model, scaler, and label encoder
    torch.save(model.state_dict(), os.path.join(models_path, 'trained_model.pth'))
    dump(scaler, os.path.join(scalers_path, 'scaler.joblib'))
    dump(label_encoder, os.path.join(label_encoders_path, 'label_encoder.joblib'))
    print("Training complete. Model, scaler, and label encoder saved.")
    model_config = {
        "input_length": X_train.shape[2],
        "num_classes": len(np.unique(y_train))
    }
    config_path = os.path.join(base_path, 'model_config.json')
    with open(config_path, 'w') as f:
        json.dump(model_config, f)

    print("Model configuration saved.")


def load_features_and_labels():
    all_songs = SongFeature.objects.all()

    features = []
    labels = []
    desired_length = 13000  # Max length for VGGish embeddings

    for song in all_songs:
        # Convert JSON strings back to lists for processing, if necessary
        spectral_contrast = np.mean(np.array(json.loads(song.average_spectral_contrast), dtype=float))
        mfccs_mean = np.array(json.loads(song.mfccs_mean), dtype=float)
        vggish_embeddings = np.array(json.loads(song.vggish_embeddings), dtype=float)

        # Adjust VGGish embeddings to have a uniform length of 100
        if len(vggish_embeddings) > desired_length:
            vggish_embeddings = vggish_embeddings[:desired_length]  # Truncate
        elif len(vggish_embeddings) < desired_length:
            # Pad with zeros
            vggish_embeddings = np.pad(vggish_embeddings, (0, desired_length - len(vggish_embeddings)), mode='constant',
                                       constant_values=0)

        song_features = [
            song.tempo,
            song.average_spectral_centroid,
            song.average_spectral_rolloff,
            spectral_contrast,
            *mfccs_mean,  # Flatten MFCCs means into the feature vector
            song.average_chroma_stft,
            song.average_rms_energy,
            *vggish_embeddings  # Now of uniform length
        ]
        features.append(song_features)
        labels.append(song.genre)

    if not features or not labels:
        print("No data found, returning None.")
        return None, None

    return np.array(features, dtype=float), np.array(labels)


def preprocess_data(features, labels):
    # Encode labels
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    # Scale features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(features_scaled, labels_encoded, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, scaler, label_encoder


def create_dataloaders(X_train, X_test, y_train, y_test, batch_size=32):
    # Convert numpy arrays to PyTorch tensors
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.long)
    y_test_tensor = torch.tensor(y_test, dtype=torch.long)

    # Create TensorDatasets
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

    # Create DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)

    return train_loader, test_loader


def train_model(model, criterion, optimizer, train_loader, test_loader, epochs=2, patience=3):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Early stopping initialization
    best_val_loss = float('inf')
    patience_counter = 0

    for epoch in range(epochs):
        model.train()  # Set model to training mode
        running_loss = 0.0
        correct_predictions = 0
        total_predictions = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            # Zero the parameter gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            # Backward pass and optimize
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs, 1)
            correct_predictions += (predicted == labels).sum().item()
            total_predictions += labels.size(0)

        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = correct_predictions / total_predictions

        print(f'Epoch {epoch + 1}/{epochs} - Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.4f}')

        # Validation step
        model.eval()  # Set model to evaluation mode
        val_running_loss = 0.0
        val_correct_predictions = 0
        val_total_predictions = 0

        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs, labels = inputs.to(device), labels.to(device)

                outputs = model(inputs)
                loss = criterion(outputs, labels)

                val_running_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                val_correct_predictions += (predicted == labels).sum().item()
                val_total_predictions += labels.size(0)

        val_epoch_loss = val_running_loss / len(test_loader.dataset)
        val_epoch_acc = val_correct_predictions / val_total_predictions

        print(f'Validation - Loss: {val_epoch_loss:.4f}, Accuracy: {val_epoch_acc:.4f}')

        # Check for early stopping
        if val_epoch_loss < best_val_loss:
            best_val_loss = val_epoch_loss
            patience_counter = 0
        else:
            patience_counter += 1

        if patience_counter >= patience:
            print("Early stopping triggered.")
            break


if __name__ == "__main__":
    train_and_save_models()
