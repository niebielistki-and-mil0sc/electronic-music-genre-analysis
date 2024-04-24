# generate_genre_image.py

import os
import openai
import requests
from django.conf import settings
from dotenv import load_dotenv

# Load environment variables from .env file at the script's start
load_dotenv()

# Load the OPENAI_API_KEY from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
print("API Key:", OPENAI_API_KEY)

# Initialize the OpenAI client with your API key
openai.api_key = OPENAI_API_KEY

# Initialize the OpenAI client with your API key
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def generate_genre_image(genre_name):
    image_path = None

    try:
        # Create a prompt for the genre
        prompt = f"Create a conceptual art piece that represents the music genre {genre_name}."

        # Call the OpenAI API to generate the image
        response = client.images.generate(
            model="dall-e-3",  # Or "dall-e-2" depending on which model you want to use
            prompt=prompt,
            size="512x512",
            quality="standard",
            n=1
        )

        # Extract the URL of the generated image
        image_url = response.data[0].url

        # Define the path for the image
        image_path = os.path.join(settings.STATICFILES_DIRS[0], 'genre_images', f"{genre_name}.png")

        # Download the image and save it to the file system
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, 'wb') as image_file:
                image_file.write(response.content)
            print(f"Image successfully saved to {image_path}")
        else:
            print(f"Failed to download the image. HTTP status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Check if image_path has been set, otherwise print a message or handle the error
    if image_path is None:
        print("Failed to generate the image path.")
    else:
        return image_path

if __name__ == '__main__':
    genre_name = "Funk"  # Example genre for testing
    print(f"Generating image for genre: {genre_name}")
    image_path = generate_genre_image(genre_name)
    print(f"Image saved to: {image_path}")
