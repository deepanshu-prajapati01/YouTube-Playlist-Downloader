import datetime
from pymsgbox import alert
from pytube import Playlist, YouTube
from pytube.cli import on_progress  # this module contains the built in progress bar.
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
  global cache, cache_file_name, playlist_name
  # This part of code will be used to extract the urls from the playlist
  try:
    playlist = Playlist(playlist_url)
    try:
      playlist_name = playlist.title
      playlist_name = re.sub(r'[^\x00-\x7f]', '', playlist_name)
    except:
      playlist_name = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
      print("We have changed the playlist name, because of the error in retrieveing the playlist name.")
    videos_links = []
    for links in playlist:
      videos_links.append(links)
  except Exception as err_name:
    exit(alert(text=f"There is following error that occured.\n{err_name}.\nPlease report this error to the author.",
               title="YouTube-Playlist-Downloader"))

  # This part will be used to extract the title of the video and also download the video.
  os.chdir(path_to_save_files)

  if not os.path.exists(playlist_name):
    os.mkdir(playlist_name)
    os.chdir(playlist_name)
    is_cache = False
    with open(cache_file_name, 'x') as file:
      pass

  else:
    os.chdir(playlist_name)
    if os.path.exists(cache_file_name):
      with open(cache_file_name) as file:
        cache = file.read().split("\n")

  # This part of the code will be used to download the video and rename it after downloading.
  try:
    print(cache)
    for file_number, video_link in enumerate(videos_links):
      # THIS PART TO MAKE SURE DON'T DONWLOAD ANY VIDEO AGAIN.
      # Cause it is in the cache that the video has already been downloaded.

      if str(file_number) not in cache:
        yt = YouTube(video_link, on_progress_callback=on_progress)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video_name = re.sub(r'[^\x00-\x7f]', '', video.default_filename.title())
        if os.path.exists(video_name):
          # This is almost 0.0001% case that this part of the code will come to play cause there is no chance.
          # But in case there is a file with the same name, the file will be replaced.
          os.remove(video_name)

        # CODE TO DOWNLOAD THE VIDEO
        print(f"Downloading video {file_number + 1} - {video_name}")
        video.download()

        # CODE TO RENAME THE FILE IN SUCH A WAY, SO THAT THE USER KNOW THE ORDER OF THE FILE.
        os.rename(video_name, f"{file_number + 1}. {video_name}")

        # CODE TO ADD THE FILE NAME TO THE CACHE.
        with open(cache_file_name, 'a') as file:
          file.write(f"{file_number}\n")
    alert(text=f"Your playlist with the name \'{playlist_name}\' has been successfully downloaded.\n"
               f"You can access your playlist from the desired location given below.\n"
               f"{path_to_save_files}\\{playlist_name}",
          title="YouTube-Playlist-Downloader")

  except Exception as error:
    alert(text="The following error occurred during downloading the playlist:\n"
               f"{error}\n"
               "This may be due to internet.\n"
               "You can download the video again by providing the playlist\n"
               "to the program to resume downloading.",
          title="YouTube-Playlist-Downloader")


if __name__ == "__main__":
  url = input("Enter the link to your playlist to download it:  ")
  main(url)