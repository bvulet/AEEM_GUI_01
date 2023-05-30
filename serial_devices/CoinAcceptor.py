from serial_comm import pack_message, read_write_establ
import numpy as np
"""
-----------------------
    Module content
------------------------
Created for coin acceptor class definitions
includes headers, information about data
presetup of coin acceptor regarding manufacturer and
type
design by Boris Vuleta
"""

"""
Coin_acceptor_1 == Suzohap/Comestero RM5 ccTalk 
"""


class Coin_acceptor_1(object):

    """ This object is used to prepare everything for RM5 device as well
    as to configure header informations regarding manufacture documents for this device

    device_var_reg - device variable register, including header,data size to expect in reading as well as in sending,
    data type to read, what kind of information - data buffer to send to slave (None - None , 1 -Variable,
    int - integer)
    device_var_reg == header, read data size, information type (int, bool, char), what to send
    # 0 - those defined are presented in ccTalk doc but not in RM5 manual
    """

    device_var_reg = dict(
                reset_device=(1, 0, bool, None),    # nece se raditi
                req_comm_status_var=(2, 3, int, None),
                clear_comm_status_var=(3, 0, bool, None),    ##
                comms_revision=(4, 3, int, None),  # Expected: 2, 4, 2 pitanje treba li u ovom trenutku uopce
                request_coin_id=(184, 6, str, 1),  ##
                modify_coin_id=(185, 0, bool, str), # ovo ce biti zadnje nakon sto sve probamo s uredajem - programiranje coina pa bi to islo preko hmi
                build_code=(192, 8, str, None),    ##
                request_last_modif_date=(195, 2, int, None),    # ove dvije 195 i 196 su iste - upitno treba li mi uopce
                request_creation_date=(196, 2, int, None),       # 195i 196 su iste - upitno treba li mi uopce
                master_inhibit_status=(227, 1, int, None),  # 1 - coin handler enabled, 0 - coin handler disabled
                modify_master_inhibit_status=(228, 0, bool, int),  # data = 1 -coin enabled, data=0 - coin disabled - ovo zadnje napraviti
                read_buffered_credit_or_error_codes=(229, 11, int, None),
                inhibit_status=(230, 2, int, None),
                modify_inhibit_status=(231, 0, bool, int),    # ove dvije jos pregledati -za ack mozda je bolje umjesto bool definirati None - nece se koristiti
                perform_self_check=(232, 2, int, None),    # nisu kodovi definirani pogledati opis funkcije - ili bilo sto osim nule - error nije OK
                software_revision=(241, -1, str, None),     # nece se raditi
                serial_number=(242, 3, int, None),
                database_version=(243, 1, int, None),       # nece se raditi
                product_type=(244, 16, str, None),
                equip_category=(245, 3, str, None),       ##
                manufacturer_ID=(246, 16, str, None),       ##
                req_status=(248, 1, int, None),            ##
                polling_priority=(249, 2, int, None),       ##
                simple_poll=(254, 0, bool, None)           ##

                          )

    def __init__(self, serial_object, master_addr, slave_addr, device_log, verbose=False):

        self.serial_object = serial_object
        self.verbose = verbose
        self.master_addr = master_addr
        self.slave_addr = slave_addr
        self.CA_log = device_log
        self.comm_err_flag = False

    def send_inq_get_resp(self, string_header, data_to_send, add_info):

        if string_header in self.device_var_reg:
            request = self.device_var_reg[string_header]
            header = request[0]
            bytes_expected = request[1]
            type_returned = request[2]
            data = [data_to_send]
            type_send = request[3]
            #print(data_to_send)

        else:
            #log = log_to_file.program_log(__name__)
            self.CA_log.exception(f"Header {string_header} not found for request")
            #print("not found")
            self.raise_err_flag()
            return False

        pack_mess, checksum = pack_message(self.slave_addr, self.master_addr, header, data)

        # simple byte array without data
        if type_send is None:
            pack_mess_1 = bytearray(pack_mess)
            checksum = bytearray([checksum])
            pack_mess_1 = pack_mess_1 + checksum

        # upisi data u poruku
        else:
            pack_mess_1 = bytearray(pack_mess)
            checksum = bytearray([checksum])
            pack_mess_1 = pack_mess_1 + checksum

        #pack_mess_1 = self.define_byte_seq(pack_mess,header,data)

        #print("pakiran u bajtove je", pack_mess_1)
        reply_msg = read_write_establ(self.serial_object, self.master_addr, self.slave_addr, pack_mess_1, bytes_expected)

        if reply_msg is None or reply_msg == "Communication error":
            self.raise_err_flag()
            self.CA_log.exception(f"Reply message {reply_msg} for {string_header}  error")
            return None

        elif type_returned == bool:

            unpack_msg = self.ack_message_unpack(reply_msg, header)

        elif string_header == "req_status":
            unpack_msg = self.req_status_unpack(reply_msg)

        elif string_header == "polling_priority":
            unpack_msg = self.poll_prior_unpack(reply_msg)

        elif string_header == "request_coin_id":
            unpack_msg = self.reply_req_coin_id(reply_msg, data)

        elif string_header == "req_comm_status_var":
            unpack_msg = self.reply_req_comms_status(reply_msg)

        elif string_header == "serial_number":
            unpack_msg = self.reply_serial_unpack(reply_msg)

        elif string_header == "perform_self_check":
            unpack_msg = self.reply_self_check_unpack(reply_msg)

        elif string_header == "inhibit_status":
            unpack_msg = self.reply_inh_status_unpack(reply_msg)

        elif string_header == "master_inhibit_status":
            unpack_msg = self.reply_master_inhibit_status(reply_msg)

        elif string_header == "request_creation_date" or string_header == "request_last_modif_date":
            unpack_msg = self.reply_req_crdate_unpack(reply_msg)

        elif type_returned == str:

            unpack_msg = self.reply_string_unpack(reply_msg)
            #print("unpack je", unpack_msg)

        return unpack_msg

    def raise_err_flag(self):
        self.comm_err_flag = True

    def define_byte_seq(self, pack_message_, header, data):

        """Function that packs on a device level
         depending on type of a variable defined in a manual  message so that
        slave  can recognize byte sequence
         pack_message - packed message in a serial_comm which consists of int ex [1 0 3 244, xx]

         header - based on a header type function packs a message into structure,
        data - data is used to adjust it in byte sequence

        """

        return None

    def ack_message_unpack(self, reply_msg, header):
        """Function that unpacks a response for messages with just ACK. This is only for testing!!
        Maybe later for main program as a confirmation can be used"""

        r_header = int(reply_msg[3])
        mess_len = len(reply_msg)
        mess_info = 4

        if r_header == 0 and mess_len == 5:
            #print ("ACK uredan")
            return True

        else:
            #log = log_to_file.program_log(__name__)
            self.CA_log.exception(f" ACK {r_header} not right")
            return False

    def req_status_unpack(self, reply_msg):
        """Function that unpacks a response for messages that respond with int and
        their decyrption. For example header 248 coin acceptor status codes say that
         0 - OK,
         1 - coin return mechanism activated
         2- C.O.S mechanism activated."""
        r_header = int(reply_msg[3])
        r_data_size = int(reply_msg[1])
        mess_info = 4
        message_body = {}
        i = 0
        message = 0

        for i in range(r_data_size):
            message_body[i] = reply_msg[mess_info + i]
            message += message_body[i] * pow(256, i)

        if message == 0:
            device_status = "OK"

        elif message == 1:
            device_status = "Coin return mechanism activated"

        elif message == 2:
            device_status = "C.O.S mechanism activated"

        return device_status

    def poll_prior_unpack(self, reply_msg):
        """Function that unpacks a pooling priority with units and data.
        This is an indication by a device of the recommended polling interval for buffered
        credit information. Polling a device at an interval longer than this may result in lost
        credits.
        units = 0 - special, 1 -ms, 2 x10ms, 3 - seconds, 4-minutes, 5- hours, 6 - days, 7 -weeks, 8- months, 9 -years
        """
        r_header = int(reply_msg[3])
        r_data_size = int(reply_msg[1])
        mess_info = 4
        message_body = {}
        i = 0
        message = 0
        print("pooling reply is", reply_msg)
        units = dict(special=0,
                     ms=1,
                     x10ms=2,
                     sec=3,
                     min=4,
                     hour=5,
                     days=6,
                     weeks=7,
                     months=8,
                     years=9
                     )
        read_units = reply_msg[4]
        value = reply_msg[5]
        key_list = list(units.keys())
        value_list = list(units.values())

        if value in value_list:
            position = value_list.index(read_units)
            string_units = key_list[position]
            polling_result = {value, "*", string_units}
            return polling_result
        else:
            return None

    def reply_string_unpack(self, reply_msg):
        """Function that unpacks string  in bytes array.
         First it starts with extraction of message body data based on data size, then converts it to a strings"""

        #print("reply_msg_3 je",reply_msg[3])
        #r_header = int(reply_msg[3])
        #r_data_size = int(reply_msg[1])
        mess_info = 4
        message_body = {}
        message_body = reply_msg[:-1]
        message_body = reply_msg[4:len(message_body)].decode('utf-8')
        return message_body

    def reply_serial_unpack(self, reply_msg):
        """Function that unpacks a response for serial number (int) and it's decyrption.
            Function returns int multiplied with pow of 256. That is <message> """

        r_header = int(reply_msg[3])
        r_data_size = int(reply_msg[1])
        mess_info = 4
        message_body = {}
        i = 0
        message = 0

        for i in range(r_data_size):
            message_body[i] = reply_msg[mess_info + i]
            message += message_body[i] * pow(256, i)

        return message

    def reply_self_check_unpack(self, reply_msg):
        """ Function that unpacks fault codes for self check of slave device RM5
        every fault code is defined and explained in table 3 of ccTalk manual
        Because of a long list of code errors they will be evaluated later and I ll take just
        the ones needed or set it to be in int reply mode but later through program decode it"""

        r_header = int(reply_msg[3])
        r_data_size = int(reply_msg[1])
        mess_info = 4
        message_body = {}
        i = 0
        message = 0

        for i in range(r_data_size):
            message_body[i] = reply_msg[mess_info + i]
            message += message_body[i] * pow(256, i)

        return message

    def reply_inh_status_unpack(self, reply_msg):
        """ this message gets request inhibit status which in this case is 2 byte mask
        where ecah bit of byte is True or False. That array represent the state of each channel
        0 == Coin/disabled (inhibited)
        1 == coin enabled (not inhibited)
        in my case there are 6 channels  so mask one with one byte is sufficient"""
        # ovu funkciju treba pregledati dobro jer nezz radi li ova konverzija iz hex byte u bin
        r_header = int(reply_msg[3])
        r_data_size = int(reply_msg[1])
        mess_info = 4
        mess_size = len(reply_msg)
        data = (reply_msg[4:mess_size-1])

        mask_1 = data[0]
        mask_2 = data[1]
        message = list(format(mask_1, "b"))

        ch_nmbr = 1
        j = 0
        string = []
        for i in message:
            string.append("channel_"+str(ch_nmbr))
            j += 1
            ch_nmbr += 1

        channel_status = dict(zip(string, message))
        return channel_status

    def reply_req_crdate_unpack(self, reply_msg):
        """ This function unpacks creation date relative to base year ( product base year )
         Bits 15 and 14 are reserved, 9-14 for year, 5-8 for month and 0-4 to days - NIJE ZAVRSENA
         Year - relative
         Month - 1 to 12
         Day 1-31"""
        r_header = int(reply_msg[3])
        r_data_size = int(reply_msg[1])
        mess_info = 4
        data_LSB = reply_msg[4]
        data_MSB = reply_msg[5]

    def reply_req_coin_id(self, reply_msg, data_s):
        r_header = int(reply_msg[3])

        mess_len = len(reply_msg)

        mess_info = 4

        data = ["channel_"+str(data_s[0]), reply_msg[mess_info:mess_len-1].decode('utf-8')]

        return data

    def reply_req_comms_status(self, reply_msg):
        """ Request comms status variables. This function consists of 3 cumululative single byte event counter (255
        vraps to 0)
        1. rx timeouts -
        2. rx bytes ignored -
        3. rx bad checksums -
        3 bytes are located in a list of recieved data as an integers
        """
        r_header = int(reply_msg[3])
        r_data_size = (reply_msg[1])
        mess_len = len(reply_msg)
        mess_info = 4
        recieved_data = list(reply_msg[mess_info:mess_len-1])
        return recieved_data

    def reply_master_inhibit_status(self, reply_msg):
        r_header = int(reply_msg[3])
        mess_len = len(reply_msg)
        mess_info = 4
        received_data = list(reply_msg[mess_info:mess_len-1])
        return received_data

    def read_buffered_credit_or_error_codes(self, string_header, data_to_send, add_info):

        request = self.device_var_reg[string_header]
        header = request[0]
        bytes_expected = request[1]
        type_returned = request[2]
        data = [data_to_send]
        type_send = request[3]

        pack_mess, checksum = pack_message(self.slave_addr, self.master_addr, header, data)

        pack_mess_1 = bytearray(pack_mess)
        checksum = bytearray([checksum])
        pack_mess_1 = pack_mess_1 + checksum

        reply_msg = read_write_establ(self.serial_object, self.master_addr, self.slave_addr, pack_mess_1, bytes_expected)

        if reply_msg is None or reply_msg == "Communication error":
            self.raise_err_flag()
            self.CA_log.exception(f"Reply message {reply_msg} for {string_header}  error")
            return None

        r_header = int(reply_msg[3])
        mess_len = len(reply_msg)
        mess_info = 4
        #print("primljeni bajtovi su", reply_msg)
        #event_count = int(reply_msg[mess_info])
        #print("event_counter je", event_count)
        received_data = list(reply_msg[mess_info:mess_len - 1])

        return received_data

    def buff_credit_or_error_codes_decy(self, data, old_data): #=[] - izbaceno iz data i old_tata
        print("data je", data)
        print("old data je", old_data)
        old_event = old_data[0]
        curr_event = data[0]
        data_new = data
        print("sad je", data_new)
        data_new = data_new[1:-1:2]
        data_old = old_data[1:-1:2]
        #curr_data = np.asarray(data_new).reshape((5, 2))
        #old_data1 = np.asarray(data_old).reshape((5, 2))
        print("sad je nakon rezanja", data_new)
        #print("data matrics je",curr_data)
        #column_size = 2
        #row_size = 6
        result = np.zeros((5, 2), dtype=int)
        print("old vs new event", old_event, curr_event)

        if (curr_event == old_event):
        #     #print("nema promjena")
            return 0

        elif curr_event == 0:
            self.CA_log.exception("Coin Acceptor Restarted")
            return 0

        elif (7 > data_new[0]> 0):
            return data_new[0]

        start_pos = curr_event % 5
        diff = curr_event - old_event

        # for i in range(0, diff):
        #
        #     for j in range(0, column_size):
        #         if 7 > curr_data[i][0] > 0:  # kanali su od 1 do 7
        #             result[i][j] = curr_data[i][j]
                    #print("result je", result)
               # elif diff ==2 and :
               #     result[i][j] = data[i][j]

        #return result
