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
device_config_file_name = "./device_config.ini"
users_config_file_name = "./user_accounts.ini"
owner_config_file_name = "./owner_informations.ini"

users_init = {"diag_user": "diag", "dev_user": "dev",
              "video_user": "video"
              }

users_pass_init = {'diag_pass': "1234", 'dev_pass': "5678",
                    "video_pass": "1234"
                    }
master_user_init = { 'mdiag_user': "diagm", 'mdev_user': "devm",
                    'mvideo_user': "videom"
                    }
master_pass_init = {'mdiag_pass': "8765", 'mdev_pass': "4321",
                    'mvideo_pass': "9876"
                    }

user_config_sections = ["master_user", "master_passwords", "users", "passwords"]



device_config_sections = ['active_devices', "currency_set", "currency_value",
                          'dual_currency', "price", "price_value", "product_selection",
                          "time_selection"
                        ]
active_devices = {"all_enable": "True", "coin_device": "True", "bill_device":"False", "printer_device": "False",
                  "hooper_device": "False", "video_commercial": "True", "air_pump": "True"}

currency_set = {"bam": "KM", "eur": "Euro", "default_currency": "bam"}
currency_value = {"km": "1", "euro": "1.95"}
dual_currency = {"dual_currency_status": "False"}

price = {"payment_enable": "True", "action_price_1_active": "False", "action_price_2_active": "False"
         }
price_value = {"reg_1": "1", "reg_2": "2",
         "action_price_1": "1", "action_price_2": "1"}

product_selection = {"charg_1": "charging_1", "charg_2": "charging_2", "air": "air_pump"}
time_selection = {"charging": "30", "time_air": "15"}
time_unit = {"hour":"H", "minute":"min", "sec": "sec"}
owner_config_sections = ['owner_informations']
owner_details = {'name': "MyCompany", "phone": "+387544", "mail": "my@mail"}


class AeemScreenApp(App, Screen):
    def __init__(self, **kwargs):
        super(AeemScreenApp, self).__init__()

    def build(self):
        get_os = GetOsPaths()
        model = AutomatedParkingManagement()
        view = ScreenManagement(Window)
        controller = Controller(get_os, logger_file_name, model, view, active_devices,
                                currency_set, currency_value, dual_currency, price, price_value,
                                product_selection, time_selection,
                                device_config_sections, device_config_file_name, owner_details,
                                owner_config_sections, owner_config_file_name)

        user_accounts = UserAccounts(view, get_os, users_init, users_pass_init,master_user_init,
                                     master_pass_init, user_config_sections, users_config_file_name)
        model.set_controller(controller)
        view.set_controller(controller, user_accounts)

        cctalk = Serial_comm(model)
        model.set_communication(cctalk)
        model.coin_inform_device()
        return view


if __name__ == "__main__":
    AeemScreenApp().run()
