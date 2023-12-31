# ne bi bilo lose odmah ovdje rijesiti upis u neki file
#korisnika

from DataHandling import DataHandling
class UserAccounts:


    def __init__(self, view, get_os,
                 users, user_pass, master_user,
                 master_user_pass, user_config_sections,
                 config_file):

        self.read_user_data = None
        self.users = users
        self.user_pass = user_pass
        self.master_user = master_user
        self.master_user_pass = master_user_pass
        self.user_config_sect = user_config_sections

        self.configuration = DataHandling(get_os, config_file)
        self.view = view


        self.read_users()


    def change_user_passwords(self, id, password):
        """ function for changing diagnostic or development user screen. Here it looks after type of password
        it will be able to insert it as a string but also will show an error if it has a lenght less than 4 or
        just numbers"""
        if len(password) > 4 and any(element.isupper() for element in password):

            if id == "_old_diag_pass":

                data = {"diag_pass": password}
                self.configuration.write_config("passwords", data)
                status = self.configuration.save_write_config()
                if status:
                    self.inform_pass_change("ok", "Diagnostic Screen")
                    self.read_users()
                else:
                    self.inform_pass_change("error", "Diagnostic Screen")

            elif id == "_old_dev_pass":

                data = {"dev_pass": password}
                self.configuration.write_config("passwords", data)
                status = self.configuration.save_write_config()
                if status:
                    self.inform_pass_change("ok", "Developer Screen")
                    self.read_users()

                else:
                    self.inform_pass_change("error", "Developer Screen")

            elif id == "_old_video_pass":

                data = {"video_pass": password}

                data = {"dev_pass": password}
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





    def read_users(self):
        self.read_user_data = self.configuration.read_config()
        if self.read_user_data == False:
            create_config = self.configuration.create_config_file(self.user_config_sect)
            if create_config:
                self.configuration.write_config("master_user", self.master_user)
                self.configuration.write_config("master_passwords", self.master_user_pass)
                self.configuration.write_config("users", self.users)
                self.configuration.write_config("passwords", self.user_pass)
                status = self.configuration.save_write_config()
                if status:
                    self.read_user_data = self.configuration.read_config()
                else:
                    raise Exception("Cannot write to user accounts ini")

            else:
                raise Exception("Cannot work with user accounts ini")

        # ovdje ce ici backup ako ne bude ovo uzmi sql
        self.set_account_info()






    def set_account_info(self):

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




    def inform_pass_change(self, state, information):
        self.view.get_screen("usercontrolscreen").popoutselect(state, information)
        self.view.get_screen("usercontrolscreen").reset_text_input()




