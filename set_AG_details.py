# This program is to add Artist and Genre to a song IF it does not have the details
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

def set_metadata(file_path, artist, genre):
    try:
        audio=MP3(file_path, ID3=EasyID3)
        audio['artist']=artist
        audio['genre']=genre
        audio.save()
        print(f"Artist and Genre updated for {file_path}")
    except Exception as e:
        print("Error updating the file")
file_path=input("Enter the path to your MP3 file: ")
artist=input("Enter the artist name: ")
genre=input("Enter the genre: ")
set_metadata(file_path, artist, genre)