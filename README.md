# ELECTRONIC MUSIC GENRE ANALYSIS 

### Overview
The **Electronic Music Genre Analysis** tool is a sophisticated web application designed to classify electronic music tracks, harnessing the capabilities of **machine learning (ML)**, **artificial intelligence (AI)**, and **digital signal processing (DSP)**. It integrates a proprietary ML model that is the product of  in-house development and training on a dataset of **over 11,500 electronic tracks**, achieving an impressive classification **accuracy of up to 95%**.

This tool employs advanced DSP methods to extract a comprehensive set of acoustic features, which are then analyzed by the ML model. This model is powered by PyTorch and leverages complex neural network architectures, including both convolutional and recurrent layers, to discern and classify a rich array of electronic music genres. The scikit-learn library further refines the model’s ability to generalize across the diverse dataset.

At its core, the application provides a nuanced genre classification across an expansive library of **more than 165 electronic music genres**. The output is not merely quantitative; it includes dynamic graphical representations that illustrate the percentage match for each genre, enhancing interpretability and user engagement.

To further enrich the user experience, the application employs the **DALL-E 3** OpenAI (ChatGPT) API, generating bespoke visual representations for each classified genre. This feature not only augments the visual appeal of the results but also provides users with an immersive way to understand the musical characteristics that define different electronic music genres.

Moreover, the platform offers additional resources, such as detailed genre descriptions sourced from music.ishkur.com and associated artist profiles. This enriches the educational aspect, making it a valuable tool for music producers, DJs, enthusiasts, educational institutions, and any electronic music listener. 

The **Electronic Music Genre Analysis** tool is not merely a technological innovation; it is a bridge connecting the complex realms of ML and AI with the expressive world of electronic music. It stands as a testament to the transformative potential at the intersection of AI and the arts, illustrating how creative expressions can be systematically analyzed and appreciated through the lens of advanced computational technologies.

### Features
- **Genre Identification**: Determine the genre of a music file with high precision.
- **Comprehensive Database**: Utilizes an extensive database of 165+ electronic music genres.
- **Graphic Display**: Visual representation of analysis results, including genre percentage breakdown.
- **Rich Descriptions**: Each genre comes with a detailed description and a custom-generated image.
- **Artist Exploration**: Discover related artists with links to their Wikipedia pages for further exploration.

### How to Use
Access the tool via [link to your server]. Upload your .mp3 file using the 'Upload File' button. The analysis results will be presented both in a percentage format and graphically on the screen.

#### How It Works

Uploading: User uploads a track in .mp3 format.
Analysis: The backend processes the audio file, extracting features relevant to musical genre.
Classification: The ML model classifies the track, comparing it to a learned dataset.
Results: The frontend displays the results, including the percentage match to various genres.

### Installation
For local development and usage:

```bash
git clone [repository-link]
cd [repository-directory]
# Install dependencies
pip install -r requirements.txt
# Run the application
python manage.py runserver
```


### Contributing

We welcome contributions from the community. Please read our CONTRIBUTING.md for guidelines on how to make a contribution.

### Developers

[Your Name]
[Collaborator's Name]
(Add links to your GitHub profiles.)

### Acknowledgments

music.ishkur.com for providing valuable genre data.
igorbrigadir/ishkurs-guide-dataset on GitHub for dataset usage.
OpenAI's ChatGPT for assisting in image generation.

### License

This project is licensed under the MIT License.

### Contact

For any queries or collaborations, please reach out to [your email].



