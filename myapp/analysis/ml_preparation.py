import os
import json  # Add this line
import numpy as np
from joblib import dump
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from django.apps import apps  # Adjusted import for Django models

# Ensure the Django environment is setup if this script is run standalone
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
import django

django.setup()

SongFeature = apps.get_model('your_app_name', 'SongFeature')  # Adjust app name and model name accordingly


def prepare_dataset_from_db():
    """
    Prepares the dataset for machine learning by retrieving extracted features from the database.
    """
    features = []
    labels = []

    # Query all SongFeature objects from the database
    all_song_features = SongFeature.objects.all()

    for song_feature in all_song_features:
        # Reconstruct the feature list from the stored data
        feature_list = [
            song_feature.tempo,
            song_feature.average_spectral_centroid,
            song_feature.average_spectral_rolloff,
            np.mean(np.array(json.loads(song_feature.average_spectral_contrast))),
            *json.loads(song_feature.mfccs_mean),
            song_feature.average_chroma_stft,
            song_feature.average_rms_energy,
        ]
        features.append(feature_list)
        labels.append(song_feature.genre)

    X = np.array(features)
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(labels)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y


def main():
    X_scaled, y = prepare_dataset_from_db()
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Initialize and train the SVM model
    model = SVC(kernel='linear')  # You can experiment with different kernels and parameters
    model.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Evaluate the model
    print("Accuracy on test set:", accuracy_score(y_test, predictions))
    print("\nClassification report:\n", classification_report(y_test, predictions))

    # Save the trained model for later use
    dump(model, 'genre_classifier.joblib')

if __name__ == "__main__":
    main()

