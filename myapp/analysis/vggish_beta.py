from torchvggish import vggish, vggish_input

# Initialize the model and put it in eval mode
embedding_model = vggish()
embedding_model.eval()

# Convert your MP3 file to WAV format and name it 'example.wav' before running this
# For the sake of this example, let's assume the conversion is done, and 'example.wav' is ready

# Preprocess the audio file to create examples
examples = vggish_input.wavfile_to_examples("/Users/milosz/Downloads/1993 - Hard Acid - Acid - Directional Force - "
                                            "Planet 42 (Spectral Emotions mix).wav")

# Forward pass to get embeddings
embeddings = embedding_model.forward(examples)

# Now, embeddings variable contains your audio features. You can process these further as needed.
print(embeddings)
