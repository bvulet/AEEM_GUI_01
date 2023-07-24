
#----------------------------------------------
# Simulation of ccTalk communication module
#----------------------------------------------

import threading
from time import sleep
import queue
from collections import deque
import random
class Serial_comm(threading.Thread):
    def __init__(self,model):
        threading.Thread.__init__(self,daemon=True)
        self.stringvar = "this"
        self.my_queue = deque([0,0,0,1,1,1])
        self.model = model
        self.coin_status_q = queue.Queue()
        self.coin_payment_q = queue.Queue()
        self._lock = threading.Lock()
        self.log_file = "devices_log.log"
        self.device_log = None


    def run(self):
        self.coin_simulation()

    def coin_simulation(self):
        counter = 0
        while True:
            if  bool((random.getrandbits(1))) is True:
                self.model.registered_amount(random.getrandbits(2),1)
            sleep(1)
            #counter += 1



    def quering(self,counter,name):
        print("puni se")
        self.my_queue.append(self.stringvar + str(counter))
        print(self.my_queue)
    def unquering(self):
        return self.my_queue.pop()


    def device_check(self):
        return 0



    def device_disable(device):
        print("u funkciji je trenutno", device)
        return device
        # if coin_bypass and bill_bypass and hooper_bypass == True:
        #     # poslati na adresu onog koji trazi ovo a zatim ACK je potvrda da je operacija uspjela
        #     # tako da ce disable confirmation biti ACK
        #
        #     pass
        #
        #     #send command to them all return True
        #
        # elif coin_bypass == True:
        #          pass                              # send command to coin bypass
        #
        # if bill_bypass == True:
        #     pass              # send command to bill
        #
        # elif hooper_bypass == True:
        #     pass
        #     # send command to hooper
        #
        # elif bill_bypass == True:
        #
        #     # send command to bill bypass
        #     if coin_bypass == True:
        #         pass
        #         # send command to coin
        #     elif hooper_bypass == True:
        #         pass
        #         # send command to hooper
        # elif hooper_bypass == True:
        #     # send command to hooper
        #     if coin_bypass == True:
        #         pass
        #         # send command to coin
        #     elif bill_bypass == True:
        #         pass
        #         # send command to hooper

