from pytube import Playlist, YouTube
from pytube.cli import on_progress #this module contains the built in progress bar.
import os, re

# To make the folder where all the files are going to be downloaded.
owner_folder = "Deepanshu-Prajapati01"
os.chdir(f"{os.path.expanduser('~')}\\Videos\\")
if not os.path.exists(owner_folder):
    os.mkdir(owner_folder)


path_to_save_files = f"{os.path.expanduser('~')}\\Videos\\{owner_folder}"
cache = []
cache_file_name = '.cache.txt'

def main(playlist_url):
    global cache, cache_file_name
    # This part of code will be used to extract the urls from the playlist
    try:
        playlist = Playlist(playlist_url)
        playlist_name = playlist.title()
        videos_links = []
        for links in playlist:
            videos_links.append(links)
    except Exception as err_name:
        return err_name
    

    #This part will be used to extract the title of the video and also download the video.
    os.chdir(path_to_save_files)
    print(playlist_name)
    
    if not os.path.exists(playlist_name):
        os.mkdir(playlist_name)