# ----------------------------
# File name APB
# Automated parking controller
# ----------------------------



from ManageVideos import ManageVideos


class Controller():

    def __init__(self, get_os, user_accounts, model, view):

        self.model = model
        self.logger = self.model.logger_start
        self.view = view
        self.os_paths = get_os
        self.user_account = user_accounts
        self.manage_videos = ManageVideos(self.view)

        self.amount_inserted = None
        self.selection_costing = None

        self.device_status = None
        self.device_code = None

        self.check_coin_bypass = False
        self.check_bill_bypass = False
        self.check_hooper_bypass = False
        self.all_bypass = False

        self.enable_payment = False

        self.video_directory = None
        self.usb_directorys = None

        self.video_dir = "video_dir"
        self.linux_rel_video_dir = ""
        self.linux_video_dir = None




    def price_set(self, id_sel, value):
        """ Used for price init or price changing directly from GUI
        """
        if id_sel == "_15_min_price":
            self.model.price_selected["min_15"] = value  # write to model
            self.check_prices()  # update screen
            self.model.write_user_config()
        elif id_sel == "_30_min_price":
            self.model.price_selected["min_30"] = value
            self.check_prices()
            self.model.write_user_config()
        elif id_sel == "_45_min_price":
            self.model.price_selected["min_45"] = value
            self.check_prices()
            self.model.write_user_config()
        elif id_sel == "_1_h_price":
            self.model.price_selected["hour_1"] = value
            self.check_prices()
            self.model.write_user_config()
        elif id_sel == "_2_h_price":
            self.model.price_selected["hour_2"] = value
            self.check_prices()
            self.model.write_user_config()
        elif id_sel == "_24_h_price":
            self.model.price_selected["hour_24"] = value
            self.check_prices()
            self.model.write_user_config()
        else:
            self.model.send_to_log("price_set_error")

    def check_reg_amount(self):

        self.model.registered_amount()

    def time_selection(self, time_selected):
        """ Used for time selection transfer in GUI and a model of APM
        :variable: time_selected as a variable from GUI to model

         """

        self.model.selected_time = time_selected
        self.selection_costing = self.model.time_select(time_selected)

        if time_selected is None:
            self.view.get_screen("naplatascreen").time_selection_show("Izabrano", "")
            self.view.get_screen("paymentscreen").time_selection_show("Selected", "")
        else:
            self.view.get_screen("naplatascreen").time_selection_show(self.model._costing,
                                                                      time_selected)  # ovo promijeniti
            self.view.get_screen("paymentscreen").time_selection_show(self.model._costing, time_selected)

    def price_check(self, amount_inserted, amount_inserted_ui):
        """ Used for sending information about inserted amount of money
        in machine"""
        # iz modela

        self.view.get_screen("naplatascreen").amountinserted(amount_inserted_ui)
        self.view.get_screen("paymentscreen").amountinserted(amount_inserted_ui)
        self.amount_inserted = amount_inserted

    def service_payment(self):
        """ Used for payment services. Depending on a user selection as well as with
        a money amount it will behave with this below options. An addition should be made in order to detect
        a malfunction or paper out and according to that to disable payment options at all."""
        if not self.model.all_disable:

            if self.selection_costing is None or self.amount_inserted is None:
                # ovo ce ici na popup screen

                self.view.get_screen(self.view.current).popoutselect("error")

            elif self.amount_inserted < self.selection_costing:

                self.view.get_screen(self.view.current).popoutselect("unsufficient")

            elif self.amount_inserted == self.selection_costing:
                # self.printer_action(1,1,1,1)
                self.model.clear_registered_amount()

                self.view.get_screen(self.view.current).popoutselect("ok")

            elif self.amount_inserted > self.selection_costing:  # pitanje je kako hooper prepoznaje koliko da vrati tipa 1x0.5 + 1*1 ili samo 1.5
                amount_to_return = self.amount_inserted - self.selection_costing
                # self.printer_action(1,1,1,1)
                self.model.return_amount(amount_to_return)
                self.view.get_screen(self.view.current).popoutselect("return")

        else:
            self.model.send_to_log("device_disabled")  # na welcome screen uredaj je u kvaru ili ugasen
            # zabrani pristup onim screenovima osim >>
            # ta ista funckija ce biti i prilikom prve provjere

    def printer_action(self, time, date, time_selection, price):
        """ Calling a printer to print a card with date and time, selected time option as well as the price
            for that selection"""

        # provjera ispravnosti uredaja nakon printanja
        self.diagnostic_ui()
        pass

    def device_check(self, disable_type):

        """ Sending commands from GUI and to GUI about disabling a device
        also it is used to write that command back to a file and set a
        device as disabled"""

        status = self.model.device_control(disable_type)

        if status == "all_disabled":

            self.view.get_screen("developerscreen").inform_disable("all_disabled")

        elif status == "all_enabled":

            self.view.get_screen("developerscreen").inform_disable("all_enabled")

        elif status == "req_error":

            self.view.get_screen("developerscreen").inform_disable("req_error")

        elif status == "unexpected_err":
            status = self.model.device_control(disable_type)
            self.model.send_to_log("device_operation_error")
            # self.view.get_screen("developerscreen").inform_disable("unexpected_err")
            # pozovi welcome screen i kazi da imamo gresku u nalogu te ne daj
            # rad uredaja odn da se ide u menije - kao i gore---

        elif status == "coin_enable":

            self.view.get_screen("developerscreen").inform_disable("coin_enable")

        elif status == "coin_disable":

            self.view.get_screen("developerscreen").inform_disable("coin_disable")

        elif status == "bill_enable":

            self.view.get_screen("developerscreen").inform_disable("bill_enable")

        elif status == "bill_disable":

            self.view.get_screen("developerscreen").inform_disable("bill_disable")

        elif status == "hooper_enable":

            self.view.get_screen("developerscreen").inform_disable("hooper_enable")

        elif status == "hooper_disable":

            self.view.get_screen("developerscreen").inform_disable("hooper_disable")

    def diagnostic_ui(self):

        self.model.device_diagnostic()
        if self.model.comm_error_flag:
            error_name = "ccTalk_communication"
            state = "Error"
            code = 0
            self.view.get_screen("diagnosticscreen").device_status(error_name, state,
                                                                   code)
        else:
            name = "ccTalk_communication"
            state = "OK"
            code = 0
            self.view.get_screen("diagnosticscreen").device_status(name, state, code)

        self.view.get_screen("diagnosticscreen").device_status(self.model.coin_device_name, self.model.coin_status,
                                                               self.model.coin_code)

        self.view.get_screen("diagnosticscreen").device_status(self.model.bill_device_name, self.model.bill_status,
                                                               self.model.bill_code)
        self.view.get_screen("diagnosticscreen").device_status(self.model.hooper_device_name, self.model.hooper_status,
                                                               self.model.hooper_code)


# ovo ce otici odavdje
    def inform_pass_change(self, state, information):
        self.view.get_screen("usercontrolscreen").popoutselect(state, information)
        self.view.get_screen("usercontrolscreen").reset_text_input()
# ovo ce otici odavdje
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





    def check_prices(self):

        id_price = list(self.model.price_selected.keys())
        price = list(self.model.price_selected.values())

        self.view.get_screen("developerscreen").show_old_prices(id_price, price, self.model.price_currency)


    def inform_first_start_device_check(self):
        if self.model.all_disable:
            self.view.get_screen('welcomescreen').disable_ui_device(self.model.all_disable)
            self.view.get_screen("developerscreen").inform_disable("all_disabled")
        else:
            self.view.get_screen('welcomescreen').disable_ui_device(self.model.all_disable)
            self.view.get_screen("developerscreen").inform_disable("all_enabled")

        if self.model.coin_disable:
            self.view.get_screen("developerscreen").inform_disable("coin_disable")
        else:
            self.view.get_screen("developerscreen").inform_disable("coin_enable")

        if self.model.bill_disable:
            self.view.get_screen("developerscreen").inform_disable("bill_disable")

        else:
            self.view.get_screen("developerscreen").inform_disable("bill_enable")

        if self.model.hooper_disable:
            self.view.get_screen("developerscreen").inform_disable("hooper_disable")

        else:
            self.view.get_screen("developerscreen").inform_disable("hooper_enable")




    def start_devices(self):

        self.model.clear_registered_amount()  # mozda promijeniti da sprema lovu





    def video_start_state(self, first_start):

        video_directory = self.os_paths.check_directory(self.video_dir) #logger

        usb_directorys = self.os_paths.get_removable_drives()


        if usb_directorys is None: # nisam siguran treba li ovo ili da ne prikaze nista
            usb_directorys = video_directory

        self.view.get_screen("videocontrolscreen").destination_folder_connect(video_directory, usb_directorys)
        self.view.get_screen("welcomescreen").video_permission_control(self.model.video_permission)
        self.view.get_screen("videocontrolscreen").inform_video_user(self.model.video_permission)

        if first_start:

            self.update_video_playlist(video_directory)

        else:
            pass


    def video_control_and_permission(self):

        if self.model.video_permission:
            self.model.video_permission = False
            self.model.write_user_config()

        else:
            self.model.video_permission = True
            self.model.write_user_config()

        self.view.get_screen("videocontrolscreen").inform_video_user(self.model.video_permission)
        self.view.get_screen("welcomescreen").video_permission_control(self.model.video_permission)


    def trigger_video_exit(self):
        self.view.get_screen("videoscreen").trigger_exit()

    def save_folder_managing(self, copied_path, paste_path):
       self.view.get_screen("videocontrolscreen").inform_user(
           self.os_paths.save_folder_managing(copied_path, paste_path))

    def delete_folder_managing(self, directory):
        self.view.get_screen("videocontrolscreen").inform_user(
            self.os_paths.delete_folder_managing(directory))


    def update_video_playlist(self, playlist_directory):
        self.view.get_screen("videoscreen").video_directory(
            self.manage_videos.update_video_playlist(playlist_directory))

    def unload_video_file(self):
        self.view.get_screen("videoscreen").unload_video()
