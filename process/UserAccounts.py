# ne bi bilo lose odmah ovdje rijesiti upis u neki file
#korisnika

class UserAccounts:

    diag_master_pass = "8765"
    diag_master_user = "diag_master"

    dev_master_pass = "4321"
    dev_master_user = "dev_master"

    video_master_user = "video_master"
    video_master_pass = "9876"


    def __init__(self, view, model):

        self.diag_pass = "1234"
        self.diag_user = "diag"
        self.dev_pass = "5678"
        self.dev_user = "dev"
        self.video_user = "video"
        self.video_pass = "1234"
        self.view = view
        self.model = model
        self.set_account_info()

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


    def set_account_info(self):

        self.view.get_screen("loginscreen").account_setup(self.model.dev_user, self.model.dev_pass,
                                                          self.model.diag_user, self.model.diag_pass,
                                                          self.model.video_user, self.model.video_pass)

        self.view.get_screen("loginscreen").master_account_setup(self.model.dev_master_user, self.model.dev_master_pass,
                                                                 self.model.diag_master_user,
                                                                 self.model.diag_master_pass,
                                                                 self.model.video_master_user,
                                                                 self.model.video_master_pass)