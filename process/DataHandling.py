import sys
import os.path
import log_to_file
from distutils.util import strtobool


class DataHandling:

    data_config_headers = ["passwords", "peripheral_status",
                           "peripheral_code", "current_price", "current_currency"]

    def __init__(self, get_os_type, logger_file_name, device_config_file_name):
        self.os_type = get_os_type
        self.logg_name = logger_file_name
        self.dev_conf_name = device_config_file_name
        self.passwords = {'diag':None, "dev":None, "video":None}
        self.device_periph_stat = {"bills":None, "hooper":None, "coin":None, "video_perm":None}
        self.billing_data = {"currency": None, "price_normal":None, "price_custom":None}

    def init_logger(self):
        filename = "APM_logger.log"
        set_file = os.path.join(self.logger_path, self.logg_name)
        self.logger_start = log_to_file.file_log(__name__, set_file,
                                                 "D", 2, 90, 'utf-8')
        self.logger_start.info("Logger initialization")

    def read_user_config(self):

        """read user configuration from a file for
            a bypass, disable, price_selected"""

        try:

            with open(self.dev_conf_name, ) as f:
                self.config.read(self.dev_conf_name)

        except FileNotFoundError:
            self.send_to_log("user_config_not_found")
            create = self.create_config_file()
            if create:
                self.write_user_config()
        # ovdje ces iteracijom ubaciti sve ovo prema dictionary vrijednostima i onom u config file-u
        # kao i u write user config funkciji

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




    def create_config_file(self):
        try:
            with open(self.config_file_name,"x") as f:
                f.write()
                return True

        except FileNotFoundError:
            exit()

