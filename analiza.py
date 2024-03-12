import librosa
import numpy as np


def analyze_mp3(file_path):
    # Load the audio file
    y, sr = librosa.load(file_path, sr=None)

    # Spectral Features: Centroid, Rolloff, and Contrast can give a good indication of the spectral shape and distribution.
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

    # Rhythm Feature: Tempo, as it's fundamental in distinguishing between genres.
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    # Timbre Feature: MFCCs, as they capture the timbral texture of the music.
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfccs_mean = np.mean(mfccs, axis=1)

    # Harmony Feature: Chroma, to understand the harmonic content.
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)

    # Energy Feature: RMS, to measure the energy of the audio signal.
    rms = librosa.feature.rms(y=y)

    # Print extracted feature averages as a summary.
    print(f"Tempo: {tempo} beats per minute")
    print(f"Average Spectral Centroid: {np.mean(spectral_centroids)}")
    print(f"Average Spectral Rolloff: {np.mean(spectral_rolloff)}")
    print(f"Average Spectral Contrast: {np.mean(spectral_contrast, axis=1)}")
    for i, mfcc_mean in enumerate(mfccs_mean, 1):
        print(f"MFCC {i}: {mfcc_mean}")
    print(f"Average Chroma STFT: {np.mean(chroma_stft, axis=1)}")
    print(f"Average RMS Energy: {np.mean(rms)}")


# Example usage
file_path = '/Users/milosz/Desktop/ishkur/Funk/Commodores - Machine Gun.mp3'
analyze_mp3(file_path)
