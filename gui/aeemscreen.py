#------------------------------
# File name aeemscreen.py
#------------------------------
# manager for custom screen events

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from time import strftime

#---------------------------------
# set screen properties
#----------------------------------



Builder.load_file('gui/welcomescreen.kv')
Builder.load_file('gui/payment.kv')
Builder.load_file('gui/backgroundscreen.kv')
Builder.load_file('gui/naplata.kv')
Builder.load_file('gui/diagnosticscreen.kv')
Builder.load_file('gui/loginscreen.kv')
Builder.load_file('gui/initscreen.kv')
Builder.load_file('gui/developerscreen.kv')
Builder.load_file('gui/usercontrolscreen.kv')
Builder.load_file('gui/videoscreen.kv')
Builder.load_file('gui/videocontrolscreen.kv')
class ScreenManagement(ScreenManager,Screen):

    def __init__(self,Window, **kwargs):
        super(ScreenManagement, self).__init__()
        self.timer = None
        self.window = Window
        Clock.schedule_interval(self.update_time,0)
        self.controller = None
        self.cyclic_update = None
        self.splash_screen()



    def set_controller(self,controller):

        self.controller = controller
        self.cyclic_update= Clock.schedule_interval(self.cyclic_update_amount, .5)


    def cyclic_update_amount(self, *kvargs):

        self.controller.check_reg_amount()




    def splash_screen(self):
        self.current = 'initscreen'
        self.on_enter_screen()



    def update_time(self, nap):

        self.get_screen("welcomescreen").ids._backgroundscreen.time.text = strftime('%m/%d/%Y, %H : %M : %S')
        self.get_screen("naplatascreen").ids._backgroundscreen.time.text = strftime('%m/%d/%Y, %H : %M : %S')
        self.get_screen("paymentscreen").ids._backgroundscreen.time.text = strftime('%m/%d/%Y, %H : %M : %S')
        self.get_screen("diagnosticscreen").ids._backgroundscreen.time.text = strftime('%m/%d/%Y, %H : %M : %S')
        self.get_screen("loginscreen").ids._backgroundscreen.time.text = strftime('%m/%d/%Y, %H : %M : %S')
        self.get_screen("developerscreen").ids._backgroundscreen.time.text = strftime('%m/%d/%Y, %H : %M : %S')
        self.get_screen("usercontrolscreen").ids._backgroundscreen.time.text = strftime('%m/%d/%Y, %H : %M : %S')


    def callbackTowelcome(self, *args):

        # return to main screen
        self.current = 'welcomescreen'

    def on_enter_screen(self, *args):
        # start the timer for 30 seconds

        if self.current =='loginscreen' or self.current =='diagnosticscreen'or self.current == 'developerscreen':

            self.timer = Clock.schedule_once(self.callbackTowelcome, 30)

        elif self.current == 'videoscreen':
            Clock.unschedule(self.callbackTowelcome)

        else:

            self.timer = Clock.schedule_once(self.callbackTowelcome, 20)

    def on_leave_screen(self, *args):
        # cancel the timer
        Clock.unschedule(self.callbackTowelcome)
        self.timer = None

    def on_touch_down(self, touch):
        if self.timer is not None:
            Clock.unschedule(self.callbackTowelcome)
        # reset the timer
        if self.current =='loginscreen' or self.current =='diagnosticscreen' or self.current == 'developerscreen':

            self.timer = Clock.schedule_once(self.callbackTowelcome, 30)

        else:

            self.timer = Clock.schedule_once(self.callbackTowelcome, 20)
        return super(ScreenManagement, self).on_touch_down(touch)

