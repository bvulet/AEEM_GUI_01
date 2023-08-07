# ---------------------------
# file name App.py
# --------------------------
# Main app script used to start all

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.config import Config
from aeemscreen import ScreenManagement
from APM import AutomatedParkingManagement
from APB import Controller
from device_control import SerialDevices
from cctalk import Serial_comm
from UserAccounts import UserAccounts
from GetOsPaths import GetOsPaths
import os

# ---------------------------------
# set screen properties
# ----------------------------------
os.environ["KIVY_AUDIO"] = "sdl2"
os.environ["KIVY_VIDEO"] = "ffpyplayer"
Window.clearcolor = (1, 1, 1, 1)
Window.borderless = True
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', '0')
Config.set('input', 'mouse', 'mouse, disable_multitouch')
Config.write()

# sve postavke direktorija i videa ce biti ovdje

#------------------------------------
#  Program parameters
#------------------------------------
logger_file_name = "APM_logger.log"
device_config_file_name = "./user.ini"
users_config_file_name = "./user_accounts.ini"


users_init = {"diag_user": "diag", "dev_user": "dev",
              "video_user": "video"
              }

users_pass_init = {'diag_user': "1234", 'dev_user': "5678",
                    "video_user": "1234"
                    }
master_user_init = { 'diag_user': "diagm", 'dev_user': "devm",
                    'video_user': "videom"
                    }
master_pass_init = {'diag_user': "8765", 'dev_user': "4321",
                    'video_user': "9876"
                    }

user_config_sections = ["master_user", "master_passwords", "users", "passwords"]

class AeemScreenApp(App, Screen):
    def __init__(self, **kwargs):
        super(AeemScreenApp, self).__init__()

    def build(self):
        get_os = GetOsPaths()
        model = AutomatedParkingManagement()
        view = ScreenManagement(Window)
        controller = Controller(get_os, logger_file_name, model, view,
                                users_init, users_pass_init, master_user_init,
                                master_pass_init, user_config_sections, users_config_file_name,
                                device_config_file_name)
        model.set_controller(controller)
        view.set_controller(controller)

        cctalk = Serial_comm(model)
        model.set_communication(cctalk)
        model.coin_inform_device()
        return view


if __name__ == "__main__":
    AeemScreenApp().run()
