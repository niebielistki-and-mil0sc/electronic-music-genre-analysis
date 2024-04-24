# ELECTRONIC MUSIC GENRE ANALYSIS

## Overview
The Electronic Music Genre Analysis application is a state-of-the-art platform that merges deep learning, digital signal processing, and web development to classify electronic music tracks into a wide range of genres. Developed using a dataset of over 11,500 tracks and featuring an extensive genre database, this tool exemplifies the intersection of artificial intelligence and musicology.

## Key Technologies
- **Deep Learning**: Utilizing PyTorch for constructing the neural network models to process and analyze audio data.
- **Digital Signal Processing**: Librosa library is used for audio signal processing, extracting features such as Mel-frequency cepstral coefficients (MFCCs), spectral centroid, and chroma-stft necessary for classification.
- **Machine Learning**: scikit-learn is employed for additional machine learning processes that aid in the classification and analysis tasks.
- **Web Development**: Django and Django REST framework provide the backend infrastructure, while React is used for crafting a responsive and interactive frontend.
- **Database Management**: Django ORM is used for efficient database queries and management, handling a large dataset that includes genre information, artist details, and track features.
- **Asynchronous Task Queue**: Celery with Redis as the broker is implemented for handling long-running analysis tasks without blocking the main server thread.

## Detailed Operation
1. **Audio File Processing**: Upon file upload, the backend server written in Django accepts the .mp3 file and processes it using the Librosa library, which extracts various audio features.
2. **Feature Analysis**: Features like MFCC, spectral contrast, and beat information are used as inputs for the trained machine learning model.
3. **Genre Classification**: The machine learning model, trained on a substantial dataset with PyTorch, classifies the audio file by comparing features against known genre profiles.
4. **Results Delivery**: A JSON response containing the classification results, genre descriptions, and associated images is sent back to the frontend.
5. **Interactive Visualization**: The frontend, designed with React, interprets the results and presents them through an interactive UI where users can see the percentage breakdown of different genres and read about them.

## Application and Use Cases
- **Music Categorization**: Assisting music platforms in automatically categorizing tracks by genre.
- **Music Production**: Helping producers understand the genre composition of their works.
- **Educational Tool**: Serving as an educational platform for music students to learn about genre characteristics and history.

## Getting Started
For instructions on setting up a local development environment, deploying the application, and a detailed breakdown of the project structure, refer to the [Installation](#installation) and [Project Structure](#project-structure) sections.

## Codebase Overview
```plaintext
electronic-music-genre-analysis/
|-- frontend/               # React application
|   |-- src/
|   |   |-- components/     # React components
|   |   |-- hooks/          # React custom hooks
|   |   `-- ...
|   `-- package.json        # Frontend dependencies
|-- backend/                # Django application
|   |-- api/                # REST API endpoints
|   |-- ml_model/           # Machine learning model definitions
|   |-- services/           # Business logic for audio processing
|   `-- ...
`-- data/
    `-- genre_images/       # Image dataset for genre visualization
