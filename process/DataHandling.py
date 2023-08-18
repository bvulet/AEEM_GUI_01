import sys
import os.path
import log_to_file
from distutils.util import strtobool
from configparser import ConfigParser

class DataHandling:

    data_config_headers = ["passwords", "peripheral_status",
                           "peripheral_code", "current_price", "current_currency"]

    def __init__(self, get_os_type, config_file_name):
        self.config = ConfigParser()
        self.os_type = get_os_type
        self.logg_name = None#logger_file_name
        self.config_file_name = config_file_name
        self.read_data = dict()


    def init_logger(self):
        filename = "APM_logger.log"
        set_file = os.path.join(self.logger_path, self.logg_name)
        self.logger_start = log_to_file.file_log(__name__, set_file,
                                                 "D", 2, 90, 'utf-8')
        self.logger_start.info("Logger initialization")

    def read_config(self):

        """read user configuration from a file for
            a bypass, disable, price_selected"""

        try:

            with open(self.config_file_name, ) as f:
                self.config.read(self.config_file_name)

        except FileNotFoundError:
            return False

        for each_section in self.config.sections():
            for (each_key, each_val) in self.config.items(each_section):
                self.read_data[each_key] = each_val

        return self.read_data

    def read_section(self, section):
         return self.config.items(section)

    def write_config(self, write_section, data):

        for each_section in self.config.sections():
            if (write_section == each_section):
                for (key, value) in data.items():
                    self.config.set(write_section, str(key), str(value))

    def write_single_config(self, write_section, name, data):

        for each_section in self.config.sections():
            if (write_section == each_section):
                    self.config.set(write_section, str(name), str(data))

    def save_write_config(self):
        try:
            with open(self.config_file_name, 'w') as f:
                self.config.write(f)
            return True
        except FileNotFoundError:
            return False

    def create_config_file(self, sections):

        for each_section in sections:
            self.config.add_section(str(each_section))
        try:
            with open(self.config_file_name,"x") as f:
                self.config.write(f)
            return True

        except FileNotFoundError:
            exit()

