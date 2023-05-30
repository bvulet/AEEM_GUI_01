

import sys
import os.path
from pathlib import Path
import win32api
import win32con
import win32file
import shutil

class GetOsPaths:
    def __init__(self):
        self.os_type = None
        self.asset_path = None
        self.rel_path = None
        self.check_operating_system()
        self.rel_dir = "aps_data"
        self.lin_rel_path = "var/lib"
        self.def_dir_name = "def_dir"


    def check_operating_system(self):
        if sys.platform.startswith('win32'):
            self.os_type = 'win'
            self.rel_path = os.path.expanduser('~')


        elif sys.platform.startswith('linux'):
            self.os_type = 'linux'
            self.rel_path = self.lin_rel_path


    def check_directory(self, directory): #logger
        """ Function which checks if there is a file
        for  directory. First it checks for a type of a
        system, then it uses a command to check if exists. If yes, pass, if no,
        create it."""

        dir = os.path.join(self.rel_path, self.rel_dir, directory)
        isdir = os.path.isdir(dir)
        if isdir:
            return dir
        else:
            try:
                os.makedirs(dir)
                return dir

            except OSError:
                # directory already exists or error creating occured because of user settings
                #logger.info("directory_creation_error")
                dir = self.default_dir(directory)
                return dir
                # set default directory


    def default_dir(self,  directory):

        mod_path = Path(__file__).parent.parent
        def_directory = (mod_path / self.def_dir_name/ directory).resolve()
        return def_directory



    def get_removable_drives(self):

        if self.os_type =='win':
            drives = [i for i in win32api.GetLogicalDriveStrings().split('\x00') if i]
            rdrives = [d for d in drives if win32file.GetDriveType(d) == win32con.DRIVE_REMOVABLE]
            if not rdrives:
                return None
            else:
                return str(rdrives[0])






    def save_folder_managing(self, copied_path, paste_path):

        try:
            shutil.copy(str(copied_path), str(paste_path))
            return(1)

        except OSError:
            return(2)


    def delete_folder_managing(self, directory):

        try:
            os.remove(directory)
            return(1)

        except OSError as error:
            return(2)


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
