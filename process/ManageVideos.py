
import sys
import os.path
from pathlib import Path
import win32api
import win32con
import win32file
import shutil


class ManageVideos:
  def __init__(self, view):

    self.view = view

  def update_video_playlist(self, playlist_directory):

        types = ('.mp4', '.avi')  # the tuple of file types
        video_source = []
        files_grabbed = []

        if len(os.listdir(playlist_directory)) == 0:

            mod_path = Path(__file__).parent.parent
            playlist_directory = (mod_path / "def_dir" / "video_dir").resolve()
            files_grabbed = os.listdir(str(playlist_directory))

        else:

            for file_type in os.listdir(playlist_directory):

                if file_type.endswith(types):

                    files_grabbed.extend([file_type])

                else:

                    mod_path = Path(__file__).parent.parent
                    playlist_directory = (mod_path / "def_dir" / "video_dir").resolve()
                    files_grabbed = os.listdir(str(playlist_directory))

        for index in range(len(files_grabbed)):
            value = files_grabbed[index]
            video_source.extend([os.path.join(playlist_directory, value)])

        return video_source
