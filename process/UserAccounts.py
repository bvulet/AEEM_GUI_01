# ne bi bilo lose odmah ovdje rijesiti upis u neki file
#korisnika

from DataHandling import DataHandling
class UserAccounts:

    diag_master_pass = "8765"
    diag_master_user = "diag_master"

    dev_master_pass = "4321"
    dev_master_user = "dev_master"

    video_master_user = "video_master"
    video_master_pass = "9876"


    def __init__(self, view, model, get_os,
                 users, user_pass, master_user,
                 master_user_pass, user_config_sections,
                 config_file):

        self.users = users
        self.user_pass = user_pass
        self.master_user = master_user
        self.master_user_pass = master_user_pass
        self.user_config_sect = user_config_sections

        self.configuration = DataHandling(get_os, config_file)
        self.view = view
        self.model = model

        self.read_users()
        self.set_account_info()

#ici ce iz view prema logeru koji ce promijeniti sifru
    def change_user_passwords(self, id, password):
        """ function for changing diagnostic or development user screen. Here it looks after type of password
        it will be able to insert it as a string but also will show an error if it has a lenght less than 4 or
        just numbers"""
        if len(password) > 4 and any(element.isupper() for element in password):
            if id == "_old_diag_pass":

                self.model.diag_pass = password
                self.user_accounts()
                self.model.write_user_config()
                self.inform_pass_change("ok", "Diagnostic Screen")


            elif id == "_old_dev_pass":

                self.model.dev_pass = password
                self.user_accounts()
                self.model.write_user_config()
                self.inform_pass_change("ok", "Developer Screen")


            elif id == "_old_video_pass":
                if len(password) > 4 and any(element.isupper() for element in password):
                    self.model.video_pass = password
                    self.user_accounts()
                    self.model.write_user_config()
                    self.inform_pass_change("ok", "Video Screen")
                else:
                    self.inform_pass_change("req_error", "Video Screen")
            else:
                self.inform_pass_change("fat_error", "error")
        else:
            self.inform_pass_change("req_error", "Diagnostic Screen")

    def read_users(self):
        read_user_data = self.configuration.read_config()
        if read_user_data == False:
            create_config = self.configuration.create_config_file(self.user_config_sect)
            if create_config:
                self.configuration.write_config("master_user", self.master_user)
                self.configuration.write_config("master_passwords", self.master_user_pass)
                self.configuration.write_config("users", self.users)
                self.configuration.write_config("passwords", self.user_pass)
                self.configuration.save_write_config()
                read_user_data = self.configuration.read_config()
            else:
                raise Exception( self.user_config_sect)





    def set_account_info(self):

        self.view.get_screen("loginscreen").account_setup(self.model.dev_user, self.model.dev_pass,
                                                          self.model.diag_user, self.model.diag_pass,
                                                          self.model.video_user, self.model.video_pass)

        self.view.get_screen("loginscreen").master_account_setup(self.model.dev_master_user, self.model.dev_master_pass,
                                                                 self.model.diag_master_user,
                                                                 self.model.diag_master_pass,
                                                                 self.model.video_master_user,
                                                                 self.model.video_master_pass)
    #ici ce iz logera prema ovoj klasi
    def inform_pass_change(self, state, information):
        self.view.get_screen("usercontrolscreen").popoutselect(state, information)
        self.view.get_screen("usercontrolscreen").reset_text_input()




