# music_analysis/analysis.py
import librosa
import numpy as np


def analyze_mp3(file_path):
    """
    Analyzes an MP3 file and prints out various audio features.

    Args:
        file_path (str): The path to the MP3 file to analyze.
    """
    # Load the audio file
    y, sr = librosa.load(file_path, sr=None)

    # Spectral Features: Centroid, Rolloff, and Contrast for spectral shape and distribution.
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

    # Rhythm Feature: Tempo, fundamental in distinguishing between genres.
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    # Timbre Feature: MFCCs for the timbral texture of the music.
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfccs_mean = np.mean(mfccs, axis=1)

    # Harmony Feature: Chroma for understanding the harmonic content.
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)

    # Energy Feature: RMS to measure the energy of the audio signal.
    rms = librosa.feature.rms(y=y)

    # Compile results into a dictionary
    analysis_results = {
        'tempo': tempo,
        'average_spectral_centroid': np.mean(spectral_centroids),
        'average_spectral_rolloff': np.mean(spectral_rolloff),
        'average_spectral_contrast': np.mean(spectral_contrast, axis=1),
        'mfccs_mean': mfccs_mean.tolist(),  # Convert numpy array to list for JSON serialization
        'average_chroma_stft': np.mean(chroma_stft, axis=1),
        'average_rms_energy': np.mean(rms)
    }

    # Optionally, print the results
    for feature_name, value in analysis_results.items():
        if isinstance(value, list):
            print(f"{feature_name}:")
            for i, val in enumerate(value, 1):
                print(f"  {i}: {val}")
        else:
            print(f"{feature_name}: {value}")

    return analysis_results


# Example usage
if __name__ == "__main__":
    file_path = '/path/to/your/mp3_file.mp3'
    analyze_mp3(file_path)
