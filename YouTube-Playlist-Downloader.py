import datetime
from pymsgbox import alert
from pytube import Playlist, YouTube
from pytube.cli import on_progress  # this module contains the built in progress bar.
import os, re

# code from github to fix error 400 bad request and get_throttling_function_name: could not find match for multiple"
from pytube.innertube import _default_clients
from pytube import cipher
import re

_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]



def get_throttling_function_name(js: str) -> str:
    """Extract the name of the function that computes the throttling parameter.

    :param str js:
        The contents of the base.js asset file.
    :rtype: str
    :returns:
        The name of the function used to compute the throttling parameter.
    """
    function_patterns = [
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    #logger.debug('Finding throttling function name')
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            #logger.debug("finished regex search, matched: %s", pattern)
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )

cipher.get_throttling_function_name = get_throttling_function_name



# To make the folder where all the files are going to be downloaded.
owner_folder = "Deepanshu-Prajapati01"
os.chdir(f"{os.path.expanduser('~')}\\Videos\\")
if not os.path.exists(owner_folder):
  os.mkdir(owner_folder)

path_to_save_files = f"{os.path.expanduser('~')}\\Videos\\{owner_folder}"
cache = []
cache_file_name = '.cache.txt'

def remove_invalid_char(file_name):
  file_name = re.sub(r'[^\x00-\x7f]', '', file_name)
  file_name = re.sub(r'&', '', file_name)
  file_name = re.sub(r"|", '', file_name)
  file_name = re.sub(r":", '', file_name)
  file_name = re.sub(r",", '', file_name)
  file_name = re.sub(r"`", '', file_name)
  file_name = re.sub(r"~", '', file_name)
  file_name = re.sub(r"@", '', file_name)
  file_name = re.sub(r"$", '', file_name)
  file_name = re.sub(r"%", '', file_name)
  file_name = re.sub(r"^", '', file_name)
  file_name = re.sub(r"&", '', file_name)

  return file_name

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
    alert(text=f"There is following error that occured.\n{err_name}.\nPlease report this error to the author.",
          title="YouTube-Playlist-Downloader")
    exit(input("\n\n\nEnter any key to exit..."))

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
    print(videos_links)
    for file_number, video_link in enumerate(videos_links):
      # THIS PART TO MAKE SURE DON'T DOWNLOAD ANY VIDEO AGAIN.
      # Cause it is in the cache that the video has already been downloaded.

      if str(file_number) not in cache:
        yt = YouTube(video_link, on_progress_callback=on_progress)
        try:
          video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
          print(video)
          print("error not here")

        except:
          try:
            video = yt.streams.filter(progressive=True, only_video=True).order_by('resolution').desc().first()
          except:
            video = yt.streams.filter(only_video=True).order_by('resolution').desc().first()

        video_name = video.default_filename.title()
        video_name = remove_invalid_char(video_name)

        if os.path.exists(video_name):
          # This is almost 0.0001% case that this part of the code will come to play cause there is no chance.
          # But in case there is a file with the same name, the file will be replaced.
          os.remove(video_name)

        # CODE TO DOWNLOAD THE VIDEO
        print(f"Downloading video {file_number + 1} - {video_name}")
        video.download(filename=f"{file_number + 1}. {video_name}")

        # CODE TO RENAME THE FILE IN SUCH A WAY, SO THAT THE USER KNOW THE ORDER OF THE FILE.

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