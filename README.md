# ELECTRONIC MUSIC GENRE ANALYSIS 

> ✨ **Website URL:** *Coming soon...*


### PROJECT OVERVIEW
The **Electronic Music Genre Analysis** tool is a sophisticated web application designed to classify electronic music tracks, harnessing the capabilities of **machine learning (ML)**, **artificial intelligence (AI)**, and **digital signal processing (DSP)**. It integrates a proprietary ML model that is the product of  in-house development and training on a dataset of **over 11,500 electronic tracks**, achieving an impressive classification **accuracy of up to 94,8%**.

This tool employs advanced DSP methods to extract a comprehensive set of acoustic features, which are then analyzed by the **ML model**. This model is powered by **PyTorch** and leverages complex neural network architectures, including both convolutional and recurrent layers, to discern and classify a rich array of electronic music genres. The **scikit-learn** library further refines the model’s ability to generalize across the diverse dataset.

At its core, the application provides a nuanced genre classification across an expansive library of **more than 165 electronic music genres**. The output is not merely quantitative; it includes dynamic graphical representations that illustrate the percentage match for each genre, enhancing interpretability and user engagement.

To further enrich the user experience, the application employs the **DALL-E 3 OpenAI API**, generating bespoke visual representations for each classified genre. This feature not only augments the visual appeal of the results but also provides users with an immersive way to understand the musical characteristics that define different electronic music genres.

Moreover, the platform offers additional resources, such as detailed genre descriptions sourced from **Ishkur's Guide to Electronic Music** and associated artist profiles. This enriches the educational aspect, making it a valuable tool for music producers, DJs, enthusiasts, educational institutions, and any electronic music listener. 

The **Electronic Music Genre Analysis** tool is not merely a technological innovation; it is a bridge connecting the complex realms of ML and AI with the expressive world of electronic music. It stands as a testament to the transformative potential at the intersection of AI and the arts, illustrating how creative expressions can be systematically analyzed and appreciated through the lens of advanced computational technologies.

### FEATURES OVERVIEW
- **Advanced Machine Learning Model.** At the heart of our application lies a robust machine learning model, trained on over 11,500 tracks across more than 165 distinct genres of electronic music. This model achieves an impressive accuracy rate of up to 94,8%, allowing it to reliably identify and classify a broad spectrum of electronic music genres. Utilizing a convolutional neural network architecture, our model processes audio features to discern nuanced differences between genres, even among closely related styles.

- **Comprehensive Audio Feature Extraction.** Using the librosa library, a powerhouse in audio analysis, our application extracts a variety of features from each music track. These include tempo, spectral centroid, spectral rolloff, spectral contrast, Mel-frequency cepstral coefficients (MFCCs), chroma frequencies (chroma_stft), and root mean square (rms) energy. These features capture both the textural and timbral characteristics of the music, providing a rich dataset from which the machine learning model can learn.
- **Integration of VGGish for Deep Audio Embeddings.** Complementing our use of librosa, we employ the VGGish model, which is adept at transforming raw audio into informative embeddings. These embeddings encapsulate higher-level auditory patterns that might not be captured fully by traditional feature extraction methods, enhancing our model’s understanding and sensitivity to complex audio inputs.
- **Dynamic Genre Visualization and Description.** Each identified genre is not only displayed in terms of its classification probability but is also accompanied by a visually appealing image and a concise description. These images are dynamically generated using OpenAI's DALL-E, a state-of-the-art image generation model, ensuring that each genre visualization is unique and representative. This integration not only enriches the user interface but also aids in educational and exploratory purposes, allowing users to visually connect with the music's stylistic elements.
- **Educational Value and User Engagement.** Beyond genre classification, our platform serves as an educational tool that enriches the user’s understanding of electronic music. For each classified genre, the application provides historical insights, key characteristics, and notable artists associated with that genre. This feature is particularly useful for music producers, DJs, educators, and enthusiasts who wish to deepen their knowledge of electronic music’s diverse landscape.

### TECHNOLOGY STACK
Below is an overview of the core technologies implemented in our project, each chosen for its ability to support specific aspects of our application:

- **Django:** Utilized as our primary web framework for backend development, Django facilitates a clean and pragmatic design. In our project, it is responsible for managing database operations, serving as the structure for our models, views, and controllers, and handling URL routing. 
- **React:** Chosen for the frontend development, React enables us to create a responsive and interactive user interface. It helps in efficiently updating and rendering components that react to user actions, providing a seamless experience when users upload files and receive genre predictions. 
- **PyTorch:** This is our core framework for developing the machine learning model. PyTorch offers dynamic neural network generation, which is crucial for our application's need to process and analyze complex audio data effectively. It supports the entire pipeline from model creation, training, evaluation, and making predictions. 
- **Django Rest Framework (DRF):** DRF is used to build a clean and powerful API service, handling HTTP requests and responses. It simplifies the task of connecting our React frontend to the Django backend, enabling the efficient transmission of data for file uploads and genre predictions. 
- **Librosa:** A Python package integrated for audio analysis, librosa provides the tools for extracting various audio features such as spectral centroids, chroma features, and MFCCs which are essential for training our machine learning model. 
- **VGGish:** Employed to extract deep audio embeddings, VGGish complements Librosa by providing a higher level of abstraction in feature extraction which enhances the model's accuracy and reliability in genre classification. 
- **Libraries:** Our project also makes use of a variety of other Python libraries such as **NumPy** for handling large arrays and matrices, **Scikit-learn** for additional machine learning utilities like data pre-processing, and **Pandas** for data manipulation and analysis.

### DATA COLLECTION AND MODEL TRAINING

Our data collection sourced from various databases, including _**Ishkur's Guide to Electronic Music**_, involved comprehensive audio feature extraction using the **librosa library** for tempo, spectral characteristics, and timbral features, supplemented by **VGGish** embeddings to capture abstract audio representations.
The preprocessing pipeline normalized these features using **scikit-learn's StandardScaler** and encoded genre labels numerically with **LabelEncoder**. The model training was executed on a **convolutional neural network (CNN)**, tailored for audio data and implemented in **PyTorch**, using Cross-Entropy Loss and Adam optimizer to manage learning efficiency and minimize overfitting.
Our **Django**-**based** database schema, defining the SongFeature and GenreInfo models, supports robust data management, storing extensive track features and detailed genre information. This setup not only enhances the model’s training efficacy but also enriches the platform's educational utility. This methodical approach ensures that our tool achieves high accuracy in genre classification while maintaining scalability and depth in musical analysis.


### QUICK START
Our tool is readily available for immediate preview and testing on our dedicated server. This allows potential users and collaborators to experience the application's capabilities without the need to set up a local environment. **Here is the link to access the application.** For those interested in a more hands-on approach or who wish to contribute to the project, follow the steps below to set up and run the application locally.

#### INSTALLATION
1. **Clone the Repository.** Begin by cloning the repository to your local machine. Use the command:
```bash
git clone [repository-url]
```

2. **Install Dependencies.** Navigate into the project directory and install the required dependencies. If you are using pip, you can install all the dependencies listed in requirements.txt by running:
```bash
pip install -r requirements.txt
```
3. **Database Setup.** Our application uses Django's default SQLite database, which requires no additional setup. Simply run the following command to apply migrations and prepare the database:
```bash
python manage.py migrate
```
4. **Environment Variables.** Ensure that all necessary environment variables are set up. This includes any API keys and database settings. These can typically be stored in a .env file at the root of the project

### USAGE
Interacting with the **Electronic Music Genre Analysis** tool is designed to be straightforward and user-friendly, focusing on providing in-depth genre analysis with minimal user input. Here's how to utilize the genre prediction feature effectively:

**1.** **Uploading an audio file.**
- Navigate to the main page of the application. You'll find an **UPLOAD FILE** button prominently displayed. 
- Click on the **UPLOAD FILE** button and select any **.mp3** file from your device. _Currently, the application supports .mp3 format only._
- Once you select a file, the application immediately begins the analysis process. The upload and analysis are optimized for quick processing, ensuring you don't wait long.

<img width="1554" alt="Screenshot 2024-05-06 at 12 59 03" src="https://github.com/niebielistki-and-mil0sc/electronic-music-genre-analysis/assets/151925931/13e93b3e-b8aa-4c16-92c4-aa5f407934ce">

**2.** **Viewing the analysis results.**
- After the analysis is complete, the results are dynamically displayed on the screen. You'll see a colored bar representing the percentage match of the detected genres.
  - **Percentage contribution:** A graphical representation showing how much the song matches the genre.
  - **Genre name:** The identified genre name.
  - **Dedicated AI-generated image:** An image that visually represents the genre, generated by our integration with the OpenAI's DALL-E API.
  - **Genre description:** An excerpt from the genre description sourced from music.ishkur.com, along with a link to read the full description on the **_Ishkur's Guide to Electronic Music_** website.
  - **Associated artists:** A list of artists commonly associated with the genre. Clicking on an artist's name opens their Wikipedia page in a new tab.

<img width="1686" alt="Screenshot 2024-04-23 at 14 18 35" src="https://github.com/niebielistki-and-mil0sc/electronic-music-genre-analysis/assets/151925931/f4c3064c-ad01-442c-9528-75e71ebc29f1">

**3.** **Handling multiple genres.**
- If the application detects multiple genres in a single track, it displays a detailed breakdown for each genre. The results are ordered from the highest to the lowest percentage contribution, allowing you to understand the diverse influences in the track

**4.** **Analyzing more tracks.**
- To analyze another track, simply click the **UPLOAD FILE** button again. This allows for continuous interaction with the application, enabling you to analyze multiple tracks in a session.


### LICENSE
The **Electronic Music Genre Analysis** tool is released under the MIT License. This open-source license permits wide-ranging freedom for use, modification, distribution, and private use. It is one of the most flexible and permissive licenses, chosen to encourage the use and dissemination of this tool across various domains and projects. For full license text, users are encouraged to view the LICENSE file included in the repository.


### CREDITS AND ACKNOWLEDGEMENTS
We extend our deepest gratitude to several resources that have made the **Electronic Music Genre Analysis** tool possible:

#### Ishkur's Guide to Electronic Music
This [amazing website](https://music.ishkur.com) was an invaluable resource for our project, providing extensive genre descriptions and a comprehensive grid of artists, songs, and connections between genres. The information gathered here formed a fundamental part of our database and inspired the educational aspect of our tool. 

#### igorbrigadir/ishkurs-guide-dataset
We are particularly thankful to **igorbrigadir**, whose GitHub repository was instrumental in expediting our data collection process. This repository can be found [here](https://github.com/igorbrigadir/ishkurs-guide-dataset) and has been a crucial resource for obtaining structured genre data.

#### OpenAI
Our project utilizes **OpenAI's DALL-E API** to generate unique and thematic images for each music genre, enhancing the visual appeal and informational value of our genre analysis.

#### Community contributions
We appreciate the Python and machine learning communities for their open-source libraries such as Django, React, PyTorch, and Librosa, which have been pivotal in building this application.


### DEVELOPERS

The **Electronic Music Genre Analysis** tool is the product of a two-person team, driven by a shared passion for music and an eagerness to explore the intersections of technology and artistic expression. Our collaboration sprang from a mutual desire to apply cutting-edge machine learning techniques to the rich and diverse world of electronic music, making it accessible and educative for enthusiasts and professionals alike.

**For inquiries, support, or contributions, please connect with us through our GitHub profiles:**
- [@mil0sc](https://github.com/mil0sc)
- [@niebielistki](https://github.com/niebielistki)


