# -----------------------------------
# File name APM
# automated parking management model
# -----------------------------------

from collections import deque
from configparser import ConfigParser
import sys
import os.path
import win32api
import win32con
import win32file
from distutils.util import strtobool
from pathlib import Path
import log_to_file
from GetOsPaths import GetOsPaths


class AutomatedParkingManagement:

    def __init__(self):

        self.config = ConfigParser()
        self.os_paths = GetOsPaths()

        self.selected_time = None
        self.timer = None
        self.communication = None
        self.comm_error_flag = False
        self.coin_status_q = None
        self.costing = None
        self._costing = None
        self.inserted_amount = 0
        self.controller = None
        self.payment_queue = deque()
        self.payment_cum = None
        self.payment_cum_ui = None
        self.coin_payment_q = None
        self.all_bypass = False
        self.all_disable = False
        self.price_currency = " KM"
        self.coin_device_name = "coin_validator"
        self.coin_status = None
        self.bill_device_name = "bill_validator"
        self.bill_status = None
        self.hooper_device_name = "hooper_validator"
        self.hooper_status = None
        self.config_device_status = ['bill_status', 'coin_status', 'hooper_status']
        self.config_device_bypass = ['bill_bypass', 'coin_bypass', 'hooper_bypass']
        self.config_device_code = ['bill_code', 'coin_code', 'hooper_code']
        self.config_device_peripheral = ['video_permission']
        self.diag_master_pass = "8765"
        self.diag_master_user = "diag_master"
        self.dev_master_pass = "4321"
        self.dev_master_user = "dev_master"
        self.video_master_user = "video_master"
        self.video_master_pass = "9876"
        self.win_rel_dir = "aps_data"
        self.lin_rel_dir = "aps_data"

        self.logger_path = None
        self.abs_log_path = None
        self.logger_start = None
        # -------------------------------------------
        # will be sent to a file to read user config
        # ------------------------------------------
        self.diag_pass = "1234"
        self.diag_user = "diag"
        self.dev_pass = "5678"
        self.dev_user = "dev"
        self.video_user = "video"
        self.video_pass = "1234"

        self.coin_disable = False
        self.bill_disable = False
        self.hooper_disable = False

        self.coin_bypass = False
        self.bill_bypass = False
        self.hooper_bypass = False

        self.coin_code = "1"
        self.hooper_code = "0"
        self.bill_code = "0"

        self.video_permission = True

        self.price_selected = {'min_15': 0.5,
                               'min_30': 1,
                               'min_45': 1.5,
                               'hour_1': 2,
                               'hour_2': 3,
                               'hour_24': 7

                               }

        self.initializaton()

    def initializaton(self):
        logger_folder = "loggers"
        self.logger_path = self.os_paths.check_directory(logger_folder)
        self.read_user_config()
        self.init_logger()

    def init_logger(self):
        filename = "APM_logger.log"
        set_file = os.path.join(self.logger_path, filename)
        self.logger_start = log_to_file.file_log(__name__, set_file,
                                                 "D", 2, 90, 'utf-8')
        self.logger_start.info("Logger init")

    def read_user_config(self):
        """read user configuration from a file for
            a bypass, disable, price_selected"""

        try:

            with open('./user.ini', ) as f:
                self.config.read('./user.ini')

        except FileNotFoundError:
            self.send_to_log("user_config_not_found")
            self.write_user_config()

        self.bill_disable = (self.config.getboolean('device_disabled', self.config_device_status[0]))
        self.coin_disable = bool(strtobool(self.config.get('device_disabled', self.config_device_status[1])))
        self.hooper_disable = bool(strtobool(self.config.get('device_disabled', self.config_device_status[2])))

        self.bill_bypass = bool(strtobool(self.config.get('device_bypass', self.config_device_bypass[0])))
        self.coin_bypass = bool(strtobool(self.config.get('device_bypass', self.config_device_bypass[1])))
        self.hooper_bypass = bool(strtobool(self.config.get('device_bypass', self.config_device_bypass[2])))
        self.video_permission = bool(strtobool(self.config.get('device_peripheral', self.config_device_peripheral[0])))

        self.bill_code = self.config.get('device_code', self.config_device_code[0])
        self.coin_code = self.config.get('device_code', self.config_device_code[1])
        self.hooper_code = self.config.get('device_code', self.config_device_code[2])

        for key in self.price_selected.keys():
            self.price_selected[key] = float(self.config.get("Price", key))

        self.dev_pass = self.config.get('user_passwords', self.dev_user)
        self.diag_pass = self.config.get('user_passwords', self.diag_user)
        self.video_pass = self.config.get('user_passwords', self.video_user)
        self.device_status()

    def write_user_config(self):

        """ write user configuration to a file"""
        self.config['user_passwords'] = {
            self.diag_user: self.diag_pass,
            self.dev_user: self.dev_pass,
            self.video_user: self.video_pass
        }

        self.config['device_disabled'] = {
            self.config_device_status[0]: self.bill_disable,
            self.config_device_status[1]: self.coin_disable,
            self.config_device_status[2]: self.hooper_disable
        }

        self.config['device_bypass'] = {
            self.config_device_bypass[0]: self.bill_bypass,
            self.config_device_bypass[1]: self.coin_bypass,
            self.config_device_bypass[2]: self.hooper_bypass
        }

        self.config['device_peripheral'] = {
            self.config_device_peripheral[0]: self.video_permission

        }

        self.config['device_code'] = {
            self.config_device_code[0]: self.bill_code,
            self.config_device_code[1]: self.coin_code,
            self.config_device_code[2]: self.hooper_code
        }
        if not self.config.has_section('Price'):
            self.config.add_section('Price')

        for key in self.price_selected.keys():
            self.config.set('Price', key, str(self.price_selected[key]))

        self.device_status()

        with open('./user.ini', 'w') as f:
            self.config.write(f)

    def device_status(self):
        """ current device status upon start of a device"""

        if self.coin_disable and self.bill_disable and self.hooper_disable:
            self.all_bypass = True
            self.all_disable = True

        else:
            self.all_bypass = False
            self.all_disable = False

    def time_select(self, time):

        if time in self.price_selected:
            self.costing = self.price_selected[time]
            self._costing = str(self.costing) + self.price_currency  # send to gui
            return self.costing
        else:
            return None

    def registered_amount(self):

        """ Will be called from a ccTalk communication part when a change occures in
            one of a payment devices with another thread
            :var - cost_value, cost_det_trigger
            calls a controller to express that a trigger about change occurred and that he needs
            to update the screen.
            provjeriti sto s obradom tih vrijednosti hoce li ovdje dolaziti samo kao neki brojevi ili slozeni
            """
        old_cum = self.payment_cum

        if not self.coin_payment_q.empty():
            amount = self.coin_payment_q.get()
            print("amount je", amount)
            self.payment_queue.append(amount)
            print("payment que je", self.payment_queue)
            self.payment_cum = sum(self.payment_queue)
            print("cum je", self.payment_cum)
            self.payment_cum_ui = str(self.payment_cum) + self.price_currency
            self.controller.price_check(self.payment_cum, self.payment_cum_ui)
            if old_cum != self.payment_cum:
                self.controller.trigger_video_exit()

    def clear_registered_amount(self):

        """ After proccess done clear the queue and wait for another trigger in registered amount method"""
        self.payment_queue.clear()
        self.payment_cum = None

    def return_amount(self,
                      return_amount):  # ukoliko hooper ima neku potvrdu onda ce se iskoristiti da se vrati na clear registered_amount

        """ if controller detects that more money is inserted will call this
        funtion in order to make a callback to hooper and return the money needed. Hooper will return some confirmation
        if needed but that is for later
        :var - return_amount - as a amount needed to be returned"""
        pass

    def set_controller(self, controller):

        self.controller = controller
        # posalji pocetno stanje uredaja kontroleru

    def set_communication(self, communication):
        self.communication = communication
        self.coin_status_q = communication.coin_status_q
        self.coin_payment_q = communication.coin_payment_q

    def device_control(self, disable_type):

        """ Check for devices that are defined in ui or controller to se if they are ok.
            function works as a compiler for raw data returned from device control and forwards
            it back to controller"""

        device_status = self.communication.device_control(disable_type)
        if device_status:
            if disable_type == 'all' and device_status == "all_disabled":
                self.all_disable = True
                self.coin_disable = True
                self.bill_disable = True
                self.hooper_disable = True
                self.write_user_config()
                return "all_disable"

            elif disable_type == 'all' and device_status == 'all_enabled':
                self.all_disable = False
                self.coin_disable = False
                self.bill_disable = False
                self.hooper_disable = False
                self.write_user_config()

                return "all_enable"

            if disable_type == 'coin' and device_status == [0]:
                self.coin_disable = True
                self.write_user_config()
                return "coin_disable"

            elif disable_type == 'coin' and device_status == [1]:
                self.coin_disable = False
                self.write_user_config()
                return "coin_enable"

            if disable_type == 'bill' and device_status == [0]:
                self.bill_disable = False
                self.write_user_config()
                return "bill_disable"

            elif disable_type == 'bill' and device_status == [1]:
                self.bill_disable = True
                self.write_user_config()
                return "bill_enable"

            if disable_type == 'hooper' and device_status == [0]:
                self.hooper_disable = False
                self.write_user_config()
                return "hooper_disable"

            elif disable_type == 'hooper' and device_status == [1]:
                self.hooper_disable = True
                self.write_user_config()
                return "hooper_enable"

        else:
            self.send_to_log("model_disable_error")
            return "unexpected_err"

    # cisto dijagnostika uredaja

    def device_diagnostic(self):

        self.comm_error_flag = self.communication._comm_error_flag

        if not self.coin_disable:

            self.coin_code = self.communication.check_diagnostic1("coin_check")

            if self.coin_code == 0:  # provjeriti sto ce ova funkcija vratiti
                self.coin_status = "OK"
            else:

                self.coin_status = "Error"

        else:
            self.coin_status = "No_response"
        
        if not self.bill_disable:
            # self.communication.check_diagnostic1("bill_check")
            if self.bill_code == "0":   #provjeriti sto ce ova funkcija vratiti
                self.bill_status = "OK"
            else:
                self.bill_status = "Error"

        else:
            self.bill_status = "No_response"

        if not self.hooper_disable:
            #self.communication.check_diagnostic1("hooper_check")
            if self.hooper_code == "0":  # provjeriti sto ce ova funkcija vratiti
                self.hooper_status = "OK"
            else:
                self.hooper_status = "Error"

        else:
            self.hooper_status = "No_response"
        # posalji u screen da je disable i da njega ne provjerava !!!

    def coin_inform_device(self):
        self.controller.inform_first_start_device_check()

    def send_to_log(self, event):
        self.logger_start.info(event)

