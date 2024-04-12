# download_songs_ishkur.py
import csv
import requests
import os
import urllib.parse
from concurrent.futures import ThreadPoolExecutor


# Function to construct URL
def construct_url(row):
    genre = urllib.parse.quote(f"{row['genre']} -")
    year = urllib.parse.quote(f"({row['year']})")
    artist = urllib.parse.quote(row['artist'])
    title = urllib.parse.quote(row['title'])
    url = f"https://music.ishkur.com/music/{genre} {year} {artist} - {title}.mp3"
    return url


# Function to download song
def download_song(url, folder, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder, filename), 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename} to {folder}")
    else:
        print(f"Failed to download {filename}. Status code: {response.status_code}")


# Function to handle the download of a single row
def handle_row(row, genres, base_folder):
    if row['genre'] in genres:
        song_url = construct_url(row)
        # Added "scene" to the filename
        filename = f"{row['year']} - {row['genre']} - {row['scene']} - {row['artist']} - {row['title']}.mp3".replace(
            "/", "-")
        genre_folder = os.path.join(base_folder, row["genre"])
        if not os.path.exists(genre_folder):
            os.makedirs(genre_folder)
        download_song(song_url, genre_folder, filename)


# Main function to process CSV and download songs using multithreading
def process_and_download(csv_file_path, genres, max_workers=5):
    base_folder = '/Users/milosz/Desktop/ishkur'
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # Using ThreadPoolExecutor to download songs concurrently
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submitting tasks to the executor
            for row in reader:
                executor.submit(handle_row, row, genres, base_folder)


# Specify the path to your CSV file and genres to filter and download
csv_file_path = '/Users/milosz/Desktop/ishkur/ishkur-songs.csv'
selected_genres = ['Dancepunk', 'Filthy Electrohouse', 'Electroclash', 'Hi NRG', 'Synthpop', 'Synthwave', 'Spacesynth',
                   'Eurobeat', 'Asian Pop', 'Nu Italo', 'Eurodance', 'Handsup', 'Vocal Trance', 'Dutch House',
                   'Anthem House', 'Eurotrance', 'German Trance', 'Hard Trance', 'Hardstyle', 'Jumpstyle',
                   'UK Hardhouse', 'NRG', 'Tech Trance', 'Progressive Trance', 'Neo Trance', 'Trance',
                   'Balearic Trance', 'Dream Trance', 'Progpsy', 'Full On', 'Darkpsy', 'Psychedelic Trance',
                   'Goa Trance', 'Psydub', 'EBM', 'Futurepop', 'New Beat', 'Darkwave', 'Ethereal', 'Industrial Rock',
                   'Aggrotech', 'Industrial', 'Collage', 'Noise', 'Breakcore', 'Drill n Bass', 'Glitch Hop', 'Glitch',
                   'Ambient Techno', 'Braindance', 'Musique Concrete', 'Minimalism', 'Krautrock',
                   'Modern Classical', 'Moog', 'Plus', 'Fakebit', 'Amiga/Tracker', 'Chiptune', 'FM',
                   'Drone', 'Dark Ambient', 'Ambient', 'New Age', 'Worldbeat', 'Chill Out', 'Indie', 'Dub', 'Trip Hop',
                   'Downtempo', 'Acid Jazz', 'New Jack Swing', 'Soul', 'Reggaeton', 'R&B', '2-Step Garage', 'Grime',
                   'Future Garage', 'Dubstep', 'Brostep', 'Speed Garage', 'Garage', 'US Deep House', 'Euro Deep House',
                   'Progressive House', 'Twinkle Prog', 'McProg', '8th Note Prog', 'Progressive', 'Minimal Prog',
                   'Deeptech', 'Fidget House', 'Tech House', 'Microhouse', 'Minimal Tech', 'UK House', 'Eurohouse',
                   'World House', 'Electrohouse', 'French House', 'Disco House', 'Italo House', 'Hip House',
                   'Hard House', 'Chicago House', 'Acid House', 'Acid', 'Freeland Breaks', 'Nu Skool Breaks',
                   'Big Beat', 'Chemical Breaks', 'Breaks', 'Progressive Breaks', 'Ragga Jungle', 'Jumpup', 'Pendulum',
                   'Drumstep', 'Darkstep', 'Neurofunk', 'Techstep', 'Microfunk', 'Darkside', 'Liquid Funk', 'Jazzstep',
                   'Atmospheric Jungle', 'Happy Hardcore', 'Freeform', 'UK Hardcore', 'Hardcore', 'Speedcore', 'Rave',
                   'Euro Techno', 'Experimental Techno', 'Schranz', 'Hard Techno', 'Bleep Techno', 'Detroit Techno',
                   'Bangin Techno', 'Dub Techno', 'Minimal Techno', 'Electro', 'Florida Breaks', 'Freestyle',
                   'Turntablism', 'Themed Rap', 'Conscious Rap', 'Dancehall', 'Rap', 'Eastcoast Rap', 'Bling',
                   'Westcoast Rap', 'Southern Rap', 'Trap', 'Crunk', 'Dirty South Rap', 'Miami Bass', 'Moombahton',
                   'Technobass', 'Ghetto Tech']

# Process the CSV and download songs for selected genres
process_and_download(csv_file_path, selected_genres)

print("Finished downloading selected genres.")
