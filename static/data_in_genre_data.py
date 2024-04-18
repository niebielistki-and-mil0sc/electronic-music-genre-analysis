import markdown
import csv
import random
import os
import re
import json
from collections import defaultdict

def normalize_genre(genre):
    return genre.strip().replace(' ', '_').replace('-', '_').lower()

def clean_artist_name(artist_name):
    # Split the artist name on " feat" (case insensitive) and take the first part
    return re.split(r'\s+feat|\s+Featuring', artist_name, flags=re.IGNORECASE)[0].strip()


# Function to parse the markdown file for descriptions
def parse_markdown_descriptions(md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        content = md_file.read()

    genre_descriptions = {}
    current_genre = None
    current_description = []
    collecting = False

    lines = content.split('\n')
    for line in lines:
        if line.startswith('## '):  # New genre header detected
            if current_genre:  # Save the previous genre's complete description
                genre_descriptions[current_genre] = '\n'.join(current_description).strip()
            current_genre = normalize_genre(line[3:])  # Update the current genre
            current_description = []  # Reset for the new genre
            collecting = True  # Start collecting description
        elif collecting:
            if line.startswith('## '):  # If another genre header starts
                collecting = False  # Stop collecting for the previous genre
            else:
                current_description.append(line)  # Append the line to the current description

    # To capture the description of the last genre in the file
    if current_genre and current_description:
        genre_descriptions[current_genre] = '\n'.join(current_description).strip()

    return genre_descriptions



# Function to generate image paths
def generate_image_paths(genre_list, base_path):
    return {genre: os.path.join(base_path, f"{genre.replace(' ', '_').lower()}.webp") for genre in genre_list}

# Function to extract artists from csv
def extract_artists(csv_file_path):
    artists_by_genre = defaultdict(list)
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            normalized_genre = normalize_genre(row['genre'])
            artist_name = clean_artist_name(row['artist'])  # Clean the artist name here
            artists_by_genre[normalized_genre].append(artist_name)
    return artists_by_genre



# Main script logic
if __name__ == "__main__":
    genre_list = [
        'Dancepunk', 'Filthy Electrohouse', 'Electroclash', 'Hi NRG', 'Synthpop', 'Synthwave', 'Spacesynth',
        'Italo Disco',
        'Eurobeat', 'Asian Pop', 'Nu Italo', 'Eurodance', 'Handsup', 'Vocal Trance', 'Dutch House', 'Anthem House',
        'Eurotrance', 'German Trance', 'Hard Trance', 'Hardstyle', 'Jumpstyle', 'UK Hardhouse', 'NRG', 'Tech Trance',
        'Progressive Trance', 'Neo Trance', 'Trance', 'Balearic Trance', 'Dream Trance', 'Progpsy', 'Full On',
        'Darkpsy',
        'Psychedelic Trance', 'Goa Trance', 'Psydub', 'EBM', 'Futurepop', 'New Beat', 'Darkwave', 'Ethereal',
        'Industrial Rock',
        'Aggrotech', 'Industrial', 'Collage', 'Noise', 'Breakcore', 'Drill n Bass', 'Glitch Hop', 'Glitch',
        'Experimental',
        'Ambient Techno', 'Braindance', 'Musique Concrete', 'Minimalism', 'Krautrock', 'Modern Classical', 'Soundtrack',
        'Moog',
        'Plus', 'Fakebit', 'Amiga/Tracker', 'Chiptune', 'FM', 'Drone', 'Dark Ambient', 'Ambient', 'New Age',
        'Worldbeat',
        'Chill Out', 'Indie', 'Dub', 'Trip Hop', 'Downtempo', 'Acid Jazz', 'Nu Jazz', 'Funk', 'New Jack Swing', 'Soul',
        'Reggaeton', 'R&B', '2-Step Garage', 'Grime', 'Future Garage', 'Dubstep', 'Brostep', 'Speed Garage', 'Garage',
        'US Deep House', 'Euro Deep House', 'Progressive House', 'Twinkle Prog', 'McProg', '8th Note Prog',
        'Progressive',
        'Minimal Prog', 'Deeptech', 'Fidget House', 'Tech House', 'Microhouse', 'Minimal Tech', 'UK House', 'Eurohouse',
        'World House', 'Electrohouse', 'French House', 'Disco House', 'Italo House', 'Hip House', 'Hard House',
        'Chicago House',
        'Acid House', 'Acid', 'Hard Acid', 'Freeland Breaks', 'Nu Skool Breaks', 'Big Beat', 'Chemical Breaks',
        'Breaks',
        'Progressive Breaks', 'Ragga Jungle', 'Jumpup', 'Pendulum', 'Drumstep', 'Darkstep', 'Neurofunk', 'Techstep',
        'Microfunk',
        'Darkside', 'Liquid Funk', 'Jazzstep', 'Atmospheric Jungle', 'Oldskool Rave Hardcore', 'Happy Hardcore',
        'Freeform',
        'UK Hardcore', 'Hardcore', 'Speedcore', 'Rave', 'Euro Techno', 'Experimental Techno', 'Schranz', 'Hard Techno',
        'Bleep Techno', 'Detroit Techno', 'Bangin Techno', 'Dub Techno', 'Minimal Techno', 'Electro', 'Florida Breaks',
        'Freestyle', 'Turntablism', 'Themed Rap', 'Conscious Rap', 'Dancehall', 'Rap', 'Eastcoast Rap', 'Bling',
        'Westcoast Rap',
        'Southern Rap', 'Trap', 'Crunk', 'Dirty South Rap', 'Miami Bass', 'Moombahton', 'Technobass', 'Ghetto Tech'
    ]

    normalized_genre_list = [normalize_genre(genre) for genre in genre_list]

    md_descriptions = parse_markdown_descriptions("/Users/wiktoria/PycharmProjects/music-project/static/genre_descriptions/v3_guide.md")
    image_paths = generate_image_paths(normalized_genre_list, "/static/genre_images")
    genre_artists = extract_artists("/Users/wiktoria/PycharmProjects/music-project/static/genre_descriptions/v3_tracks.csv")

    # Combine all data into a single dictionary
    genre_data = {
        normalize_genre(genre): {
            "description": md_descriptions.get(normalize_genre(genre), ""),
            "image": image_paths.get(normalize_genre(genre), ""),
            "readMoreLink": "https://music.ishkur.com",
            "artists": random.sample(genre_artists.get(normalize_genre(genre), []),
                                     min(10, len(genre_artists.get(normalize_genre(genre), []))))
        }
        for genre in genre_list
    }

    # Write to GenreData.js
    with open("GenreData.js", "w") as file:
        file.write("const GenreData = ")
        file.write(json.dumps(genre_data, indent=2))
        file.write(";\n\nexport default GenreData;")
