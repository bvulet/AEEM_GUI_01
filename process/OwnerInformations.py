# ne bi bilo lose odmah ovdje rijesiti upis u neki file
#korisnika

from DataHandling import DataHandling

class OwnerInformations:


    def __init__(self, view, get_os,
                 owner_informations, owner_config_sections,
                 config_file):

        self.read_device_data = None
        self.owner_config_sections = owner_config_sections
        self.owner_informations = owner_informations
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


    def read_data(self):
        self.read_device_data = self.configuration.read_config()

        if self.read_device_data == False:
            create_config = self.configuration.create_config_file(self.owner_config_sections)
            if create_config:
                self.configuration.write_config("owner_informations", self.owner_informations)
                status = self.configuration.save_write_config()
                if status:
                    self.read_device_data = self.configuration.read_config()
                else:
                    raise Exception("Cannot write to owner ini")

            else:
                raise Exception("Cannot work with owner ini")

        return self.read_device_data
        # ovdje ce ici backup ako ne bude ovo uzmi sql
        #self.set_account_info()








