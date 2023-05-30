# -----------------------------------
# File name device_control
# control and interaction between
# devices in APS system
# -----------------------------------
import os.path

import log_to_file
from CoinAcceptor import Coin_acceptor_1
import serial_comm
import time
import numpy as np
import threading
from threading import Timer
import queue


class SerialDevices:

    def __init__(self, model):
        self.model = model
        self.coin_status_q = queue.Queue()
        self.coin_payment_q = queue.Queue()
        self._lock = threading.Lock()
        self.log_file = "devices_log.log"
        self.device_log = None
        # -----------------------
        # ccTalk busbar options
        # ------------------------

        self.busbar = True
        self.busbar_clear = False
        self.port = "COM8"
        self.master_adress = 1

        # ------------------------------
        # Coin acceptor parameters
        # ------------------------------

        # this will be used for programming from HMI and as comp
        # channel is channel name
        # BA_xxx - currency
        # 1,2,3.... - channel number
        self.coin_channels = dict(channel_1=("BA_010_A", 1, 10),
                                  channel_2=("BA_020_A", 2, 20),
                                  channel_3=("BA_050_A", 3, 50),
                                  channel_4=("BA_100_A", 4, 100),
                                  channel_5=("BA_200_A", 5, 200),
                                  channel_6=("BA_500_A", 6, 500),

                                  )

        self.coin_acceptor_model = "RM5 CF"
        self.coin_dev_01 = None
        self.coin_dev_01_b_credit = None
        self.coin_disable = None
        self.coin_run = None
        self.coin_equal = 100

        self.coin_comm = serial_comm.create_open_serial_object("COM8")
        self.coin_dev_01_adress = 2
        self.init_coin_check_done = True
        self._comm_error_flag = False
        # ------------------------------
        # Bill acceptor parameters
        # ------------------------------
        self.bill_disable = False

        # ------------------------------
        # Hooper  parameters
        # ------------------------------
        self.hooper_disable = False

        # ------------------------------
        # first software  start - init
        # ------------------------------

        # a flag that says the first start occured
        self.first_start = 1
        self.device_init = 1
        self.device_ok = 0
        self.init_coin_check_done = None
        self.buff_credit = []

        self.init_logger()
        self.check_init_param()
        self.init_coin_device()

    def init_logger(self):
        abs_log_path = os.path.join(self.model.logger_path, self.log_file)
        self.device_log = log_to_file.file_log(__name__, abs_log_path, "D", 2, 90, 'utf-8')
        self.device_log.info(f"this is info logging - devices started")

    def check_comm_error_flag(self):
        # ako bilo koji uredaj digne flag zaustavi sve - problem u komunikaciji - informiraj uredaj
        if self.coin_dev_01.comm_err_flag:
            self._comm_error_flag = True
            self.device_log.info("communication error flag")

    def check_init_param(self):

        with self._lock:
            self.coin_disable = self.model.coin_disable
            self.bill_disable = self.model.bill_disable
            self.hooper_disable = self.model.hooper_disable

    def call_devices_operation(self):
        self.coin_run = RepeatedTimer(.4, self.device_running_operation)

    def init_coin_device(self):

        self.coin_dev_01 = Coin_acceptor_1(self.coin_comm, self.master_adress, self.coin_dev_01_adress, self.device_log)
        time.sleep(0.01)

        if not self.coin_disable:
            self.init_coin_check("first_start")

        else:
            pass

    def init_coin_check(self, start_type):
        self.check_comm_error_flag()
        if not self._comm_error_flag:
            comm_active = self.coin_dev_01.send_inq_get_resp("simple_poll", None, None)
            print(f"comm status je {comm_active}")
            if comm_active:

                comms_status = self.coin_dev_01.send_inq_get_resp("req_comm_status_var", None, None)
                if comms_status != 0:
                    self.coin_comm_buffer()

                time.sleep(.1)
                self_check = self.coin_dev_01.send_inq_get_resp("perform_self_check", None, None)
                print("self check is", self_check)
                time.sleep(.1)
                dev_stat = self.coin_dev_01.send_inq_get_resp("req_status", None, None)
                print("Device status is", dev_stat)
                time.sleep(.1)
                master_inh_stat = self.coin_dev_01.send_inq_get_resp("master_inhibit_status", None, None)
                print("Request master inhibit status is:", master_inh_stat)

                time.sleep(.1)
                self.coin_dev_01_b_credit = self.coin_dev_01.read_buffered_credit_or_error_codes(
                    "read_buffered_credit_or_error_codes", None, None)
                self.device_log.info("coin acceptor initiated")
                time.sleep(.1)

                self.init_coin_check_done = True

                if self.coin_disable is True and master_inh_stat[0] == 1:
                    self.coin_dev_01.send_inq_get_resp("modify_master_inhibit_status", 0, None)

                elif self.coin_disable is False and master_inh_stat[0] == 0:
                    self.coin_dev_01.send_inq_get_resp("modify_master_inhibit_status", 1, None)

                with self._lock:
                    self.model.coin_code = self_check
                    self.model.coin_status = dev_stat

                if start_type == "first_start":
                    coin_unblock = self.coin_dev_01.send_inq_get_resp("modify_master_inhibit_status", 1, None)

                    time.sleep(.1)
                    self.busbar = True
                    self.call_devices_operation()

                elif start_type == "working_condit":
                    return True

            else:
                self.init_coin_check_done = False
                with self._lock:
                    self.model.coin_code = "establ_error"
                    self.model.coin_status = "Error 01"

    def device_running_operation(self):
        self.check_comm_error_flag()
        amount_size = 0
        total_amount = 0

        # ----------------------------------------------------
        # standard regulation which checks for new inquiry
        # -----------------------------------------------------

        if self.busbar is True and not self._comm_error_flag:
            self.busbar_clear = False
            if not self.coin_disable:
                old_data = self.coin_dev_01_b_credit
                print("old data je", old_data)
                self.coin_dev_01_b_credit = self.coin_dev_01.read_buffered_credit_or_error_codes(
                    "read_buffered_credit_or_error_codes", None, None)
                # print("new data je", self.coin_dev_01_b_credit)
                coin_state = self.coin_dev_01.buff_credit_or_error_codes_decy(self.coin_dev_01_b_credit, old_data)
                print("coin state je", coin_state)
                if coin_state!=0:
                #if not np.isscalar(coin_state):
                    channel = "channel_" + str(coin_state)
                    amount = self.coin_channels[channel]
                    amount_text = amount[0]
                    amount_size = amount[2] / self.coin_equal
                    if not self.coin_payment_q.full():
                        self.coin_payment_q.put(amount_size, True, True)
                    print("Ubacio si:", amount_text)
                    total_amount = total_amount + amount_size
                    print("stanje je:", total_amount)
                    # non_zero = np.count_nonzero(coin_state)
                    # rows = 5
                    # columns = 2
                    # # provjeri stanje novcica
                    # for i in range(0, rows):
                    #     if coin_state[i][0] != 0:
                    #         # print("coin_state je", coin_state[i][0])
                    #         channel = "channel_" + str(coin_state[i][0])
                    #         # print("channel je", channel)
                    #         amount = self.coin_channels[channel]
                    #         amount_text = amount[0]
                    #         amount_size = amount[2] / self.coin_equal
                    #         if not self.coin_payment_q.full():
                    #             self.coin_payment_q.put(amount_size, True, True)
                    #         print("Ubacio si:", amount_text)
                    #         total_amount = total_amount + amount_size
                    #         print("stanje je:", total_amount)
        else:
            self.busbar_clear = True

    def devices_control(self, device_instruction):

        """ function used to enable/disable all serial devices"""
        # check master inh status da se ne razidu u nalogu i potvrdi
        coin_status = self.coin_dev_01.send_inq_get_resp("master_inhibit_status", None, None)
        if device_instruction == 'disable_all':
            coin_block = self.coin_dev_01.send_inq_get_resp("modify_master_inhibit_status", 0, None)

        elif device_instruction == 'enable_all':
            coin_block = self.coin_dev_01.send_inq_get_resp("modify_master_inhibit_status", 1, None)

    def device_control(self, device_instruction):
        """ Used to enable or disable each devices specified by the model
        in device_instruction.
        """
        self.check_comm_error_flag()
        if not self._comm_error_flag and self.coin_run:
            self.busbar = False
            while True:
                if self.busbar_clear:
                    break

            self.coin_run.stop()
            self.coin_run.thread_join()

        time.sleep(.1)

        if device_instruction == 'all':
            self.devices_control(device_instruction)

        if device_instruction == 'coin':
            # check for device_init

            if self.init_coin_check_done is None:
                first_coin_check = self.init_coin_check("working_condit")
            else:
                first_coin_check = False
            coin_status = self.coin_dev_01.send_inq_get_resp("master_inhibit_status", None, None)
            print("check status is", coin_status)

            if coin_status == [1]:  # device_instruction == 'coin_disable'
                coin_block = self.coin_dev_01.send_inq_get_resp("modify_master_inhibit_status", 0, None)
                self.coin_disable = True
                coin_status = self.coin_dev_01.send_inq_get_resp("master_inhibit_status", None, None)
                self.call_devices_operation()
                return coin_status

            elif coin_status == [0]:
                coin_unblock = self.coin_dev_01.send_inq_get_resp("modify_master_inhibit_status", 1, None)
                coin_status = self.coin_dev_01.send_inq_get_resp("master_inhibit_status", None, None)
                self.call_devices_operation()
                if coin_status:
                    self.coin_disable = False
                    self.busbar = True
                    # if first_coin_check:          # vec ce netko dignuti zastavicu
                    #     self.call_devices_operation()

                return coin_status

            #  elif device_group == 'bill':
            bill_status = 1
            if device_instruction == 'bill' and bill_status == [1]:
                bill_block = 1

            elif device_instruction == 'bill' and bill_status == [0]:
                bill_block = 0

    def check_diagnostic1(self, device):
        self.check_comm_error_flag()
        self.busbar = False

        if not self._comm_error_flag and self.coin_run:
            while True:
                if self.busbar_clear:
                    break

            if device == 'coin_check' and self.busbar_clear:
                self_check = self.coin_dev_01.send_inq_get_resp("perform_self_check", None, None)
                time.sleep(.1)
                self.busbar = True
                return self_check

    def coin_comm_buffer(self):
        # ciscenje buffera za provjeru komunikacije
        clear_comms = self.coin_dev_01.send_inq_get_resp("clear_comm_status_var", None, None)


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.daemon = True
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def thread_join(self):
        self._timer.join()
