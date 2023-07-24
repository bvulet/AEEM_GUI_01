# This is a sample Python script.
import log_to_file
from CoinAcceptor import Coin_acceptor_1
import serial_comm
import time
import numpy as np
import threading



class Serial_Devices(threading.Thread):
    def __init__(self, model):

        threading.Thread.__init__(self, daemon=True)
        self.model = model

        #--------------------------------------------
        # define constants for HMI and program
        #-------------------------------------------


        # this will be used for programming from HMI and as comp
        # channel is channel name
        # BA_xxx - currency
        # 1,2,3.... - channel number
        self.coin_channels = dict( channel_1 = ("BA_010_A", 1, 10),
                        channel_2 = ("BA_020_A", 2, 20),
                        channel_3 = ("BA_050_A", 3, 50),
                        channel_4 = ("BA_100_A", 4, 100),
                        channel_5 = ("BA_200_A", 5, 200),
                        channel_6 = ("BA_500_A", 6, 500),

                                )

        # define device name used in a product - u biti bi ovo bilo usporedi podatke uredaja s onim sto si zadao -
        # da netko ne bi mijenjao uređaj

        self.coin_acceptor_model = "RM5 CF"
        self.coin_dev_01 = None
        self.coin_dev_01_b_credit = None
        self.coin_permission = None
        self.module_log = log_to_file.file_log(__name__)
        self.module_log.info(f"this is info logging - software started")
        self.port = "COM8"
        self.coin_comm = serial_comm.create_open_serial_object(self.port)
        self.master_adress = 1
        self.coin_dev_01_adress = 2


        #------------------------------
        # first software  start - init
        #------------------------------

        # a flag that says the first start occured
        self.first_start = 1
        self.device_init = 1
        self.device_ok = 0




    def init_coin_device(self, device_permission):

        if device_permission:

            self.coin_dev_01 = Coin_acceptor_1(self.coin_comm, self.master_adress, self.coin_dev_01_adress)
            time.sleep(0.01)
            self.init_coin_check()
            self.coin_permission = device_permission

        else:
            self.coin_permission = device_permission


    def init_coin_check(self):

        equip_cat= self.coin_dev_01.send_inq_get_resp("equip_category", None, None)
        print(f"Tip uredaja je :{equip_cat}")
        time.sleep(1)

        name_dev = self.coin_dev_01.send_inq_get_resp("product_type", None, None)
        print(f"naziv je:{name_dev}")

        dev_stat = self.coin_dev_01.send_inq_get_resp("req_status", None, None)
        print("Device status is", dev_stat)

        dev_serial = self.coin_dev_01.send_inq_get_resp("serial_number", None, None)
        print("device serial number is", dev_serial)

        pooling = self.coin_dev_01.send_inq_get_resp("polling_priority",None, None)
        print("pooling priority is", pooling)

        inh_stat = self.coin_dev_01.send_inq_get_resp("inhibit_status", None, None)
        print("Inh status je", inh_stat)

        self_check = self.coin_dev_01.send_inq_get_resp("perform_self_check", None, None)
        print("self check is", self_check)

        s_pool = self.coin_dev_01.send_inq_get_resp("simple_poll", None, None)
        print("Simple pool is", s_pool)

        man_id = self.coin_dev_01.send_inq_get_resp("manufacturer_ID", None, None)
        print("man_ID je", man_id)

        master_inh_stat = self.coin_dev_01.send_inq_get_resp("master_inhibit_status", None, None)
        print("Request master inhibit status is:",master_inh_stat)

        build_code=self.coin_dev_01.send_inq_get_resp("build_code", None, None)
        print("build code is,", build_code)

        coin_id_check = self.coin_dev_01.send_inq_get_resp("request_coin_id",3, None)
        print(f" Na mjestu {coin_id_check[0]}, postavljen je:", coin_id_check[1])

        self.coin_dev_01_b_credit = self.coin_dev_01.read_buffered_credit_or_error_codes(
            "read_buffered_credit_or_error_codes", None, None)

        comms_status = self.coin_dev_01.send_inq_get_resp("req_comm_status_var",None, None)
        print(f"comm status je {comms_status}")

        self.model.coin_inform_device(man_id, dev_stat, self_check, master_inh_stat[0])


        if comms_status != 0:
            self.coin_comm_buffer()


       #     self.module_log.exception(f"Device name {name_dev} or Self-check error is, {self_check}")




    #    else:
     #       print("nesto nije ok")

        # if buff_credit == 0:
        #     log.exception(f"{name_dev} is reset as well as software")
        #     # resetiran je i uredaj i program
        # else:440
        #     log.exception("software is reset but no device")
        #

    def device_running_operation(self):
        amount_size = 0
        total_amount = 0

        #----------------------------------------------------
        # standard regulation which checks for new inquiry
        #-----------------------------------------------------

        while 1 and self.coin_permission:
            start_time = time.time()
            time.sleep(0.1)

            old_data = buff_credit
            # print("old data je", old_data)
            buff_credit = self.coin_dev_01_b_credit.read_buffered_credit_or_error_codes("read_buffered_credit_or_error_codes", None, None)
            # print("ide")
            coin_state =self.coin_dev_01_b_credit.buff_credit_or_error_codes_decy(buff_credit, old_data)

            if np.isscalar(coin_state) == False:
                # provjeri koliko elemenata nije 0
                # print("usao u if")

                non_zero = np.count_nonzero(coin_state)
                rows = 5
                columns = 2
                # provjeri stanje novcica
                for i in range(0, rows):
                    if coin_state[i][0] != 0:
                        print("coin_state je", coin_state[i][0])
                        channel = "channel_" + str(coin_state[i][0])
                        # print("channel je", channel)
                        amount = self.channels[channel]
                        amount_text = amount[0]
                        amount_size = amount[2]
                        print("Ubacio si:", amount_text)
                        total_amount = total_amount + amount_size



                # ovdje detektiraj promjenu i proslijedi na self.model.registered_amount


            # total_amount = total_amount // 100 mozda i ne raditi ovo float itd....
            print("stanje je:",total_amount)

            first_start = 0

            #print(f"time started {start_time} - --- %s seconds ---" % (time.time() - start_time))


    def devices_control(self, device_instruction):

        """ function used to enable/disable all serial devices"""
        # check master inh status da se ne razidu u nalogu i potvrdi
        coin_status = self.coin_dev_01.send_inq_get_resp("master_inhibit_status", None, None)
        if device_instruction == 'disable_all':
            coin_block = self.coin_dev_01.send_inq_get_resp("modify_master_inhibit_status", 0, None)

        elif device_instruction == 'enable_all':
            coin_block = self.coin_dev_01.send_inq_get_resp("modify_master_inhibit_status", 1, None)


    def device_control(self, device_group, device_instruction):
        """ Used to enable or disable each devices specified by the model
        in device_instruction.
        """
        if device_group == 'all':
            self.devices_control(device_instruction)


        if device_group == "coin":
            coin_status = self.coin_dev_01.send_inq_get_resp("master_inhibit_status", None, None)
            print("coin_status je", coin_status)
            if device_instruction == 'coin_disable' and coin_status == [1]:

                coin_block = self.coin_dev_01.send_inq_get_resp("modify_master_inhibit_status", 0, None)
                print("coin_block je", coin_block)
                self.coin_permission = False
                return coin_block

            elif device_instruction == 'coin_enable' and coin_status == [0]:
                coin_unblock = self.coin_dev_01.send_inq_get_resp("modify_master_inhibit_status", 1, None)
                self.coin_permission = True
                return coin_unblock

        elif device_group == 'bill':
            bill_status = 1
            if device_instruction == 'bill_disable' and bill_status == [1]:
                bill_block = 1

            elif device_instruction == 'bill_enable' and bill_status == [0]:
                bill_block = 0


    def check_diagnostic(self, device):

        if device == 'coin_check':
            self_check = self.coin_dev_01.send_inq_get_resp("perform_self_check", None, None)
            return self_check

    def coin_comm_buffer(self):

        clear_comms = self.coin_dev_01.send_inq_get_resp("clear_comm_status_var",None, None)     # ciscenje buffera za provjeru komunikacije
        # #print("ACK je clear_comms", cleart_comms)
