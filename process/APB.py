# ----------------------------
# File name APB
# Automated parking controller
# ----------------------------



from ManageVideos import ManageVideos

from DeviceRegulation import DeviceRegulation
from OwnerInformations import OwnerInformations

class Controller():

    def __init__(self, get_os, logger_file, model, view, active_devices,
                 currency_set, currency_value, dual_currency, price, price_value, product_selection,
                 time_selection, device_config_sections, config_file,
                 owner_informations, owner_config_sections, owner_config_file):

        self.model = model
        self.device_regulation = DeviceRegulation(view, get_os, active_devices, currency_set, currency_value,
                                                    dual_currency, price, price_value, product_selection,
                                                  time_selection, device_config_sections, config_file)

        self.owner_info = OwnerInformations(view, get_os, owner_informations, owner_config_sections,
                                            owner_config_file)
        self.read_owner_data = None
        self.read_device_info = None
        self.get_charging_price = None
        self.get_air_price = None

        self.logger_file = logger_file
        self.logger = self.model.logger_start
        self.view = view
        self.os_paths = get_os
        self.manage_videos = ManageVideos(self.view)

        self.amount_inserted = None
        self.selection_costing = None
        self.insert_amount = "4"
        # self.device_status = None
        # self.device_code = None
        #
        # self.check_coin_bypass = False
        # self.check_bill_bypass = False
        # self.check_hooper_bypass = False
        # self.all_bypass = False

        # self.enable_payment = False

        self.video_directory = None
        self.usb_directorys = None

        self.video_dir = "video_dir"
        self.linux_rel_video_dir = ""
        self.linux_video_dir = None
        self.read_device_parameters()
        self.read_owner_informations()

    def read_device_parameters(self):
        self.read_device_info = self.device_regulation.read_device_status()
        self.send_device_to_screen(self.read_device_info)
        self.send_payment_data_to_screen(self.read_device_info)
        self.check_active_price()

    def read_owner_informations(self):
        self.read_owner_data = self.owner_info.read_data()
        self.view.get_screen("naplatascreen").write_owner_info(self.read_owner_data)
        self.view.get_screen("paymentscreen").write_owner_info(self.read_owner_data)

    def send_device_to_screen(self, data):

        """ Sending commands from GUI and to GUI about disabling a device
              also it is used to write that command back to a file and set a
              device as disabled"""

        if data['all_enable'] != "True":

            self.view.get_screen("developerscreen").inform_screen("all_disabled")

        if data['all_enable'] == "True":
            self.view.get_screen("developerscreen").inform_screen("all_enabled")

        if data['coin_device'] == "True":

            self.view.get_screen("developerscreen").inform_screen("coin_enable")

        if data['coin_device'] == "False":

            self.view.get_screen("developerscreen").inform_screen("coin_disable")

        if data['bill_device'] == "True":

            self.view.get_screen("developerscreen").inform_screen("bill_enable")


        if data['bill_device'] == "False":

            self.view.get_screen("developerscreen").inform_screen("bill_disable")

        if data['hooper_device'] == "True":

            self.view.get_screen("developerscreen").inform_screen("hooper_enable")


        if data['hooper_device'] == "False":

            self.view.get_screen("developerscreen").inform_screen("hooper_disable")


        if data['printer_device'] == "True":

            self.view.get_screen("developerscreen").inform_screen("printer_enable")


        if data['printer_device'] == "False":

            self.view.get_screen("developerscreen").inform_screen("printer_disable")

        if data['air_pump'] == "True":

            self.view.get_screen("developerscreen").inform_screen("air_enable")


        if data['air_pump'] == "False":

            self.view.get_screen("developerscreen").inform_screen("air_disable")

        else:
            self.view.get_screen("developerscreen").inform_screen("req_error")

    def send_payment_data_to_screen(self, data):

        if data['dual_currency_status'] == "True":

            self.view.get_screen("paymentcontrolscreen").inform_screen("dual_currency_enable")

        if data['dual_currency_status'] == "False":

            self.view.get_screen("paymentcontrolscreen").inform_screen("dual_currency_disable")

        if data['payment_enable'] == "True":

            self.view.get_screen("paymentcontrolscreen").inform_screen("payment_enable")

        if data['payment_enable'] == "False":

            self.view.get_screen("paymentcontrolscreen").inform_screen("payment_disable")

        if data['action_price_1_active'] == "True":

            self.view.get_screen("paymentcontrolscreen").inform_screen("action_price_1_active")

        if data['action_price_1_active'] == "False":

            self.view.get_screen("paymentcontrolscreen").inform_screen("action_price_1_disable")

        if data['action_price_2_active'] == "True":

            self.view.get_screen("paymentcontrolscreen").inform_screen("action_price_2_active")

        if data['action_price_2_active'] == "False":

            self.view.get_screen("paymentcontrolscreen").inform_screen("action_price_2_disable")

        else:
            self.view.get_screen("paymentcontrolscreen").inform_screen("req_error")

    def check_active_price(self):
        if self.read_device_info['action_price_1_active'] == "True":
            self.get_charging_price = self.read_device_info['action_price_1']
        else:
            self.get_charging_price = self.read_device_info['reg_1']


        if self.read_device_info['action_price_2_active'] == "True":
            self.get_air_price = self.read_device_info['reg_2']
        else:
            self.get_air_price = self.read_device_info['action_price_2']



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



    def check_selected_price(self, product_type):
        if product_type == "charging_1" or product_type == "charging_2":
            time_per_unit = self.read_device_info['charging']
            price_per_unit = self.get_charging_price
            time_multi = round( float(self.insert_amount) / float(price_per_unit), 2)
            time_total = time_multi * int(time_per_unit)
            self.view.get_screen("naplatascreen").inform_time("Punjenje", time_total)
            self.view.get_screen("paymentscreen").inform_time("Charging", time_total)
        elif product_type == "air_pump":
            time_per_unit = self.read_device_info['time_air']
            price_per_unit = self.get_air_price
            time_multi = round( float(self.insert_amount) / float(price_per_unit), 2)
            time_total = time_multi * int(time_per_unit)
            self.view.get_screen("naplatascreen").inform_time("Zrak", time_total)
            self.view.get_screen("paymentscreen").inform_time("Air", time_total)





 # old
    def price_check(self, amount_inserted, amount_inserted_ui):
        """ Used for sending information about inserted amount of money
        in machine"""
        # iz modela

        self.view.get_screen("naplatascreen").amountinserted(amount_inserted_ui)
        self.view.get_screen("paymentscreen").amountinserted(amount_inserted_ui)
        self.amount_inserted = amount_inserted

    def service_payment(self, product_type):
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
#------
    def device_control(self, section, disable_type):

        """ Sending commands from GUI and to GUI about disabling a device
        also it is used to write that command back to a file and set a
        device as disabled"""

        self.read_device_info = self.device_regulation.change_values(disable_type)
        self.device_regulation.write_to_indiv_config(section, disable_type, self.read_device_info[disable_type])
        self.device_regulation.save_to_config()
        self.send_device_to_screen(self.read_device_info)
        self.send_payment_data_to_screen(self.read_device_info)
        self.check_active_price()

    def control_payment_settings(self, data):
        pass

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



    def check_prices(self):
        values = []
        def_curr = self.read_device_info['default_currency']
        get_currency = self.read_device_info[def_curr]
        get_price_section = self.device_regulation.read_section("price_value")
        for t in get_price_section:
            for item in t:
                values.append(item)

        self.view.get_screen("paymentcontrolscreen").show_old_prices(values[1:len(values):2], get_currency)



    def price_set(self, section, id_sel, value):
        """ Used for price init or price changing directly from GUI
        """
        self.device_regulation.write_to_indiv_config(section, id_sel, value)
        self.device_regulation.save_to_config()
        self.read_device_parameters()
        self.check_active_price()


#old

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
