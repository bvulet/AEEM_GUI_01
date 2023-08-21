# ne bi bilo lose odmah ovdje rijesiti upis u neki file
#korisnika

from DataHandling import DataHandling

class DeviceRegulation:


    def __init__(self, view, get_os,
                 active_devices, currency_set, currency_value,
                 dual_currency, price, price_value, product_selection,
                 time_selection, device_config_sections,
                 config_file):

        self.read_device_data = None
        self.active_devices = active_devices
        self.currency_set = currency_set
        self.currency_value = currency_value
        self.dual_currency = dual_currency
        self.device_config_sections = device_config_sections
        self.price = price
        self.price_value = price_value
        self.time_selection = time_selection
        self.product_selection = product_selection
        self.configuration = DataHandling(get_os, config_file)
        self.view = view



    def change_values(self, data_name):
        """ function for changing data regarding device configuration
        it includes change of device perihperals - enable or disable.
         Also, user can disable or enable any of devices peripheral or not regarding current status"""
        if  self.read_device_data[data_name] == "True":
            self.read_device_data[data_name] = "False"
            return self.read_device_data

        else:
            self.read_device_data[data_name] = "True"
            return self.read_device_data




    def read_device_status(self):
        self.read_device_data = self.configuration.read_config()

        if self.read_device_data == False:
            create_config = self.configuration.create_config_file(self.device_config_sections)
            if create_config:
                self.configuration.write_config("active_devices", self.active_devices)
                self.configuration.write_config("currency_set", self.currency_set)
                self.configuration.write_config("currency_value", self.currency_value)
                self.configuration.write_config("dual_currency", self.dual_currency)
                self.configuration.write_config("price", self.price)
                self.configuration.write_config("price_value", self.price_value)
                self.configuration.write_config("product_selection", self.product_selection)
                self.configuration.write_config("time_selection", self.time_selection)
                status = self.configuration.save_write_config()
                if status:
                    self.read_device_data = self.configuration.read_config()
                else:
                    raise Exception("Cannot write to device ini")

            else:
                raise Exception("Cannot work with device ini")

        return self.read_device_data


    def read_section(self, section):
        return self.configuration.read_section(section)


    def write_to_config(self, section, data):
        self.configuration.write_config(section, data)

    def write_to_indiv_config(self, section, name, data):
        self.configuration.write_single_config(section, name, data)

    def save_to_config(self):
        status = self.configuration.save_write_config()
        if status:
            self.read_device_data = self.configuration.read_config()
        else:
            raise Exception("Cannot write to device ini")





