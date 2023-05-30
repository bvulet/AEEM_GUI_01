import serial
import time
import device_control
global recieve_done
"""
----------------------
 Module content
----------------------
This module provides tools 
to open serial port, establish communication, 
check if is it open, sends a message to a device 
that uses ccTalk communication and recieves a message 
from one to a computer
This module uses parts of open source code 
and that part is highlihted
"""

license_text_open_source = "(C) 2011 David Schryer GNU GPLv3 or later."
license_text_NiVu = "(C) 2022 Boris Vuleta - NiVu."


def create_open_serial_object(port_type):

    """ this function uses parameters for ccTalk communication
    and establishes port communication with type specified in variable port_type

     Input parameters:
        port_type:str
        Type of dev to connect to:
        1.tty/USB0 - first device number


     Local variables
        baudrate : int specified by ccTalk documnentation
        parity : defined by serial library and ccTalk documentation
        stopbits: defined by ccTalk documentation
        bytesitze: defined by ccTalk documentation (8 bits)
        xonxoff: control flow on or off

    """
    port = port_type
    baudrate = 9600
    parity = serial.PARITY_NONE
    stopbits = serial.STOPBITS_ONE
    bytesize = serial.EIGHTBITS
    xonxoff = False          # communication flow control

    return serial.Serial(port=port_type,
                         baudrate=baudrate,
                         stopbits=stopbits,
                         bytesize=bytesize,
                         xonxoff=xonxoff,
                         timeout=None
                         )


def pack_message(destination_add, source_add, header, data):
    """ from data (header) value and others
    creates a ccTalk composition of message
        [ Destination Address ]
        [ No. of Data Bytes ]
        [ Source Address ]
        [ Header ]
        [ Data 1 ]
        ...
        [ Data N ]
        [ Checksum ]



    """

    #print("data sav je", data[:])
    if None in data or len(data) == 0:
        data_bytes = 0          # send none data message to a device
        # message composition
        comp = [destination_add, data_bytes, source_add, header]

    else:
        #print("ovdje si")
        data_bytes = len(data)  # number of data bytes in a message just data!
        comp = [destination_add, data_bytes, source_add, header] + data

    message_sum = 0

    for i in comp:
        message_sum += i

    end_byte = 256 - (message_sum%256)
    #print("end byte je", end_byte)

    #print("message je", comp)

    return comp, end_byte


def read_message(serial_object, sent_message, bytes_expected):

    """ Reads message from serial line - first it is message info - who sended it and to whom. Then
    data leng and header. From data lenng it is possible to get size of body message and then + 1 for chechsum.
    At the end a simple checksum for recived message is being done just to make sure everything is good."""

    #serial_object.timeout =None    # assure that request to read will not block if no mess is sent to computer
    #serial_object.inter_byte_timeout = 0.1 # ove vrijednosti s vremenskim kasnjenjem su bitne za pogledati iznova
    # kao i opcija o tome sto kad istekne vrijeme a poruka nije cjelovita ( novo slanje ili brisanje svega )

    # read mirror message or until timeout or until size expected
    sent_mess_len = len(sent_message)
    end_byte_send = bytes([sent_message[sent_mess_len - 1]])
    destination_add = bytes([sent_message[2]])      # this is for host, 1   gledajuci sa strane citanja
    source_add = bytes([sent_message[0]])              # ¸this is slave add 2,3,4
    mess_leng_exp = 5 + bytes_expected              # size of excpected message
    #print(end_byte_send)

    # wait for data needed to come-real answer or until timeout
    i = 4
    mirror_read_time = 0
    mirrored_mess = bytearray()

    # read mirrored message for cctalk communication
    # if they are the same first step is Ok, if not mess_err_flag arrives
    # breaks the loop and in 90% cases a new read is needed
    while True:
        #print("u petlji true si")
        c = serial_object.read()
        if c:
            mirrored_mess = mirrored_mess + c
            #print("mirror je", mirrored_mess)
            mirror_read_time += 1
            mirror_leng = len(mirrored_mess)

            if mirrored_mess[: sent_mess_len] == sent_message[:sent_mess_len]:
                #print("poruke su iste")
                mirr_err_flag = False
                rest_of_mess=mirrored_mess[sent_mess_len:mirror_leng]
                #print("rest of mirror is", rest_of_mess)
                break

            # elif mirrored_mess[:(sent_mess_len-1)] == sent_message[:(sent_mess_len-1)] and i==4:
            #     i=1
            #     print("tu si")

            elif mirrored_mess[:mirror_leng] != sent_message[:mirror_leng]:
                 #print("poruke do sad primljene nisu iste")
                mirr_err_flag = True
                break

        else:
            mirr_err_flag = True
            break

    # ask for a new information discard this one as not complete and as a problematic one.
    # also note to a file that this kind of situation occured - ubaciti dodatno
    if mirr_err_flag:

        m_error = 5081                                           #"Mirror message read error"
        # log = log_to_file.file_log(__name__)
        # log.exception(f" {m_error} ccTalk message error")
        return m_error

    source_dest_add = [destination_add]+[source_add]
    data_waiting_count = 0
    i = 0
    mess_info = rest_of_mess
    while True:
        data_waiting_count += 1
        #print("data waiting count", data_waiting_count)
        time.sleep(.09)
        #waiting for real data
        #print("Waiting data", serial_object.inWaiting())
        if (serial_object.inWaiting()) > 0:
           # mess_info = rest_of_mess + serial_object.read(1)
            data_waiting = serial_object.inWaiting()
            time.sleep(.05)
            mess_info = mess_info + serial_object.read(data_waiting)

            #print("data waiting", data_waiting)

            #print("nakon cekanja sam procitao", mess_info)

            if all(i in mess_info for i in source_dest_add):
                start_mess_flag = True
                star_byte_pos = mess_info.index(destination_add)
                #print("start pos je", star_byte_pos)
                read_mess_len = len(mess_info)
                #print("read_mess_len je", read_mess_len)
                break
            else:
                header_error = 5082                                    #"Source or target error"
                # log = log_to_file.file_log(__name__)
                # log.exception(f" {header_error} ccTalk message error")
                return header_error

        elif data_waiting_count == 50:
            data_arrive = 5083
            # log = log_to_file.file_log(__name__)
            # log.exception(f" {data_arrive} ccTalk message error")
            #"Data not arrived in a buffer"
            return data_arrive

    #print("mess je ", mess_info[0:read_mess_len])

    if star_byte_pos != 0:

        if read_mess_len <= 4:
            readed_len = read_mess_len - star_byte_pos-1    #1
            read_mess = mess_info[star_byte_pos:read_mess_len-1] + serial_object.read(4-readed_len)
            #print("kad 01 nije na prvom bajtu i duzina je 4",read_mess)

            data_leng = (read_mess[1])
            rest_of_mess_len = data_leng + 1
            body = serial_object.read(rest_of_mess_len)
            reply = read_mess + body

        elif read_mess_len > 4:
            readed_len = read_mess_len - star_byte_pos-1   # 1
            reply = mess_info[star_byte_pos:read_mess_len - 1] + serial_object.read(5+mess_leng_exp - readed_len)
            #print("kad 01 nije na prvom bajtu", reply)

    elif star_byte_pos == 0 and serial_object.inWaiting() > 0:
        data_leng = (mess_info[1])
        #print("data leng", data_leng)
        #print("leng je", read_mess_len)
        rest_of_mess_len = data_leng + 1
        read_mess = mess_info[star_byte_pos:read_mess_len] + serial_object.read(4+rest_of_mess_len - read_mess_len)
        #print("kad 01 je na prvom mjestu i duzina je 4", read_mess)
        reply = read_mess

    else:
        reply = mess_info
        #print(" read mess sad je", reply)

    message_sum = 0

    for i in reply:
        message_sum += i

    end_byte = 256 - (message_sum % 256)

    if end_byte % 256 == 0:   # ovo s nulom ce trebati korigirati sigurno
          #print("usao sam u provjeru checksum")
        return reply
    #
    else:
        #print("checksum primljene poruke nije dobar",  end_byte)
        chck_err = 5084
        # log = log_to_file.file_log(__name__)
        # log.exception(f" {chck_err} ccTalk message checksum error")
        #return chck_err        iz nekog razloga stvaras problem
    #print("na reply si",reply)
    return reply

def write_message(serial_object, byte_array):
    #serial_object.write_timeout = 1
    # mozda ovu funkciju ukinuti i sve staviti u read write inquiry
    print("Waiting data in", serial_object.inWaiting())
    input_buffer = serial_object.inWaiting()
    if input_buffer == 0:
        #time.sleep(.09)
        serial_object.reset_input_buffer()

    else:
       # time.sleep(.09)
        serial_object.reset_input_buffer()

    #print("Waiting data out", serial_object.out_waiting)
    #time.sleep(.09)
    serial_object.reset_output_buffer()
    #print("byte array je", byte_array)
    byte_arr_len = len(byte_array)
    byte_send_data = byte_array[0:byte_arr_len-1]

    #print("byte_send", byte_send_data)
    data_send = serial_object.write(byte_send_data)
    time.sleep(.02)
    checksum = bytearray([byte_array[byte_arr_len-1]])
    #print("checksum je", checksum)
    checksum_send = serial_object.write(checksum)

    return 1


def read_write_inquiry(serial_object, master_add, slave_add, message, bytes_expected):

    """" function to provide inquiry and read of command for serial programming level.

    message - full packed message with adresses, header, data leng, data."""

    try:
        # if not serial_object.isOpen():
        #     print("nije otvoren")
        #     msg = "not opened port"
        #     log = log_to_file.file_log(read_message)
        #     log.debug(f" {serial_object} not opened port")
        #     device_control.SerialDevices.comm_error_flag = True
        #     return None
        send_complete = write_message(serial_object, message)
        sent_message = message
        #print("poslana je")

        if send_complete == 0:
            reply_message = read_message(serial_object, sent_message, bytes_expected)

        elif send_complete != 0:
            time.sleep(0.05)
            reply_message = read_message(serial_object, sent_message, bytes_expected)

        else:
            reply_message = read_message(serial_object, sent_message, bytes_expected)

    except serial.serialutil.SerialException:

        device_control.SerialDevices.comm_error_flag = True
        return None
    return reply_message


def read_write_establ(serial_object, master_add, slave_add, message, bytes_expected):

    """ Function which is responded for calling an inquiry for send/recieve message as well
     as for checking what is a end status of that action ( error-call again or ok-close it and go to main app)
     attempting_to_send - variable responsible for error messages count
      (more than x return to main a communication error)
     """
    # dealing with communication errors
    attempting_to_send = 0
    reply_message = read_write_inquiry(serial_object, master_add, slave_add, message, bytes_expected)
    while True:

        #print("reply je", reply_message)
        if (((attempting_to_send < 4) and (reply_message == 5081 or reply_message == 5082 or reply_message == 5083 or
                                           reply_message == 5084))):
            print("prvi")
            time.sleep(.1)  #1
            reply_message = read_write_inquiry(serial_object, master_add, slave_add, message, bytes_expected)
            #print("bio si unutra",reply_message)
            attempting_to_send += 1
            #print("attempting to send =", attempting_to_send)
        elif (((attempting_to_send == 4) and (reply_message == 5081 or reply_message == 5082 or reply_message == 5083 or
                                              reply_message == 5084))):
            print("drugi")
            time.sleep(1)
            reply_message = read_write_inquiry(serial_object, master_add, slave_add, message, bytes_expected)

        elif (((attempting_to_send > 4) and (reply_message == 5081 or reply_message == 5082 or reply_message == 5083 or
                                             reply_message == 5084))):
            #print("treci")
            reply_message = "Communication error"
            break
        else:
            break

    #print("sad je", reply_message)
    return reply_message
