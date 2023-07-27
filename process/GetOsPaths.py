

import sys
import os.path
from pathlib import Path
import win32api
import win32con
import win32file
import shutil

class GetOsPaths:

    rel_dir = "aps_data"        #relative app directory
    lin_rel_path = "var/lib"    # linux relative app directory
    def_dir_name = "def_dir"    # default directory for videos and logger
    video_dir = "NiVu_def_video"



    def __init__(self):
        self.os_type = None
        self.asset_path = None
        self.rel_path = None
        self.check_operating_system()



    def check_operating_system(self):
        if sys.platform.startswith('win32'):
            self.os_type = 'win'
            self.rel_path = os.path.expanduser('~')


        elif sys.platform.startswith('linux'):
            self.os_type = 'linux'
            self.rel_path = GetOsPaths.lin_rel_path


    def check_directory(self, directory): #logger
        """ Function which checks if there is a file
        for  directory. First it checks for a type of a
        system, then it uses a command to check if exists. If yes, pass, if no,
        create it."""

        dir = os.path.join(self.rel_path, GetOsPaths.rel_dir, directory)
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
        def_directory = (mod_path / GetOsPaths.def_dir_name/ directory).resolve()
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


