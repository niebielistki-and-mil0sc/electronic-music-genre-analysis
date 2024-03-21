# downloader.py
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
        filename = f"{row['year']} - {row['genre']} - {row['scene']} - {row['artist']} - {row['title']}.mp3".replace("/", "-")
        genre_folder = os.path.join(base_folder, row["genre"])
        if not os.path.exists(genre_folder):
            os.makedirs(genre_folder)
        download_song(song_url, genre_folder, filename)

# Main function to process CSV and download songs using multithreading
def process_and_download(csv_file_path, genres, max_workers=5):
    base_folder = '/Users/wiktoria/PycharmProjects/music-project/myapp/analysis/ishkur'
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # Using ThreadPoolExecutor to download songs concurrently
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submitting tasks to the executor
            for row in reader:
                executor.submit(handle_row, row, genres, base_folder)

# Specify the path to your CSV file and genres to filter and download
csv_file_path = '/Users/wiktoria/PycharmProjects/music-project/myapp/analysis/ishkur/ishkur-songs.csv'
selected_genres = ['Funk', 'Italo Disco']

# Process the CSV and download songs for selected genres
process_and_download(csv_file_path, selected_genres)

print("Finished downloading selected genres.")
