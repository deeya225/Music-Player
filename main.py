import tkinter as tk
from tkinter import filedialog, END #Filedialog is for accessing the music folder through file explorer
import os #deals with fxns revolving around the OS e.g file&directory manipulation
import pygame #commonly used for multimedia applications e.g audio development
from PIL import Image, ImageTk  #imports the image from python libraries, used to open and display image files
from mutagen.mp3 import MP3 #imports Mp3 from the library mutagen

# Creating a tkinter window for music player
root=tk.Tk()
root.title('Music Player')
root.geometry('600x400')

pygame.mixer.init()

menu_bar=tk.Menu(root)
root.config(menu=menu_bar)

#setting variables for managing the music playlist
songs=[]
current_song=""
paused=False

song_data={} #sets an empty dictionary to store metadata

# Functions for loading, playing, pausing, and navigating songs
def load_music():
    global current_song, songs
    root.directory=filedialog.askdirectory()
    songs=[]
    for song in os.listdir(root.directory):
        name, ext=os.path.splitext(song)
        if ext=='.mp3':
            songs.append(song)
            full_path=os.path.join(root.directory, song)
            audio=MP3(full_path)
            artist=audio.tags.get('TPE1') if 'TPE1' in audio else 'Unknown artist'
            genre=audio.tags.get('TCON') if 'TCON' in audio else 'Unknown genre'
            song_data[song]={'artist': artist, 'genre': genre}
            
    songlist.delete(0,END)
    for song in songs:
        songlist.insert("end", song)
    if songs:
        current_song=songs[0]
        songlist.selection_set(0)

def play_song():
    global current_song, paused
    if current_song:
        if not paused:
            pygame.mixer.music.load(os.path.join(root.directory, current_song))
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.unpause()
            paused=False

def pause_song():
    global paused
    pygame.mixer.music.pause()
    paused=True

def forward_song():
    global current_song, paused
    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song)+1)
        current_song=songs[songlist.curselection()[0]]
        play_song()
    except:
        pass

def backward_song():
    global current_song, paused
    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song)-1)
        current_song=songs[songlist.curselection()[0]]
        play_song()
    except:
        pass

def filter_songs():
    search_type=search_by.get()
    search_value=search_entry.get().lower()
    filtered_songs=[]
    for song, meta in song_data.items():
        artist=str(meta['artist']) if 'artist' in meta else 'Unknown artist'
        genre=str(meta['genre']) if 'genre' in meta else 'Unknown genre'
        if search_type=='Artist' and search_value in artist.lower():
            filtered_songs.append(song)
        elif search_type=='Genre' and search_value in genre.lower():
            filtered_songs.append(song)

    songlist.delete(0, END)
    for song in filtered_songs:
        songlist.insert("end", song)
    if filtered_songs:
        current_song=filtered_songs[0]
        songlist.selection_set(0)
    
open=tk.Menu(menu_bar, tearoff=False)
open.add_command(label='Select Folder', command=load_music)
menu_bar.add_cascade(label='Library', menu=open)

songlist=tk.Listbox(root, bg="blue", fg="white", width=100, height=15)
songlist.pack()

controls=tk.Frame(root)
controls.pack()

# Search box for filtering
search_box=tk.Frame(root)
search_box.pack()

search_by=tk.StringVar(root)
search_by.set('Artist') # this is the default search type

search_options=tk.OptionMenu(search_box,search_by, 'Artist', 'Genre')
search_options.pack(side='left', padx=5)

search_entry=tk.Entry(search_box)
search_entry.pack(side='left', padx=5)

search_btn=tk.Button(search_box, text='Search', command=filter_songs)
search_btn.pack(side='left', padx=5)

# setting play, pause, forward and backward buttons:
def resize_img(file_path, size):
    image=Image.open(file_path)
    resized_image=image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)

play_img=resize_img(r'C:\Users\deeya\OneDrive\Desktop\MusicPlayer\images\play.png', (50,50))
pause_img=resize_img(r'C:\Users\deeya\OneDrive\Desktop\MusicPlayer\images\pause.png', (50,50))
forward_img=resize_img(r'C:\Users\deeya\OneDrive\Desktop\MusicPlayer\images\forward.png', (50,50))
backward_img=resize_img(r'C:\Users\deeya\OneDrive\Desktop\MusicPlayer\images\backward.png', (50,50))

play_btn=tk.Button(controls, image=play_img, borderwidth=0, command=play_song)
pause_btn=tk.Button(controls, image=pause_img, borderwidth=0, command=pause_song)
forward_btn=tk.Button(controls, image=forward_img, borderwidth=0, command=forward_song)
backward_btn=tk.Button(controls, image=backward_img, borderwidth=0, command=backward_song)

play_btn.grid(row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
forward_btn.grid(row=0, column=3, padx=7, pady=10)
backward_btn.grid(row=0, column=0, padx=7, pady=10)

root.mainloop()
