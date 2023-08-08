# ne bi bilo lose odmah ovdje rijesiti upis u neki file
#korisnika

from DataHandling import DataHandling

class DeviceRegulation:


    def __init__(self, view, get_os,
                 active_devices, currency_set, currency_value,
                 dual_currency, price, device_config_sections,
                 config_file):

        self.read_device_data = None
        self.active_devices = active_devices
        self.currency_set = currency_set
        self.currency_value = currency_value
        self.dual_currency = dual_currency
        self.device_config_sections = device_config_sections
        self.price = price
        self.configuration = DataHandling(get_os, config_file)
        self.view = view



    def change_values(self, id, data):
        """ function for changing data regarding device configuration
        it includes change of currency, change of prices or change of showing dual prices for
        future services. Also, user can disable or enable any of devices peripheral or not regarding current status"""
        if len(data) > 4 and any(element.isupper() for element in data):

            if id == "_old_diag_pass":

                data = {"diag_pass": data}
                self.configuration.write_config("passwords", data)
                status = self.configuration.save_write_config()
                if status:
                    self.inform_pass_change("ok", "Diagnostic Screen")
                    self.read_users()
                else:
                    self.inform_pass_change("error", "Diagnostic Screen")

            elif id == "_old_dev_pass":

                data = {"dev_pass": data}
                self.configuration.write_config("passwords", data)
                status = self.configuration.save_write_config()
                if status:
                    self.inform_pass_change("ok", "Developer Screen")
                    self.read_users()

                else:
                    self.inform_pass_change("error", "Developer Screen")

            elif id == "_old_video_pass":

                data = {"video_pass": data}

                data = {"dev_pass": data}
                self.configuration.write_config("passwords", data)
                status = self.configuration.save_write_config()
                if status:
                    self.inform_pass_change("ok", "Video Screen")
                    self.read_users()

                else:
                    self.inform_pass_change("error", "Video Screen")

            else:
                self.inform_pass_change("No ID", "error")
        else:
            self.inform_pass_change("Pass Rule Error", "Diagnostic Screen")


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
                status = self.configuration.save_write_config()
                if status:
                    self.read_device_data = self.configuration.read_config()
                else:
                    raise Exception("Cannot write to device ini")

            else:
                raise Exception("Cannot work with device ini")

        return self.read_device_data
        # ovdje ce ici backup ako ne bude ovo uzmi sql
        #self.set_account_info()






    def set_device_status(self):

        self.view.get_screen("loginscreen").account_setup(self.read_user_data['dev_user'],
                                                          self.read_user_data['dev_pass'],
                                                          self.read_user_data['diag_user'],
                                                          self.read_user_data['diag_pass'],
                                                          self.read_user_data['video_user'],
                                                          self.read_user_data['video_pass'])

        self.view.get_screen("loginscreen").master_account_setup(self.read_user_data['mdev_user'],
                                                                 self.read_user_data['mdev_pass'],
                                                                 self.read_user_data['mdiag_user'],
                                                                 self.read_user_data['mdiag_pass'],
                                                                 self.read_user_data['mvideo_user'],
                                                                 self.read_user_data['mvideo_pass'])




    def inform_change(self, state, information):
        self.view.get_screen("usercontrolscreen").popoutselect(state, information)
        self.view.get_screen("usercontrolscreen").reset_text_input()




