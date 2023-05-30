# -------------------------------
# File name diagnosticscreen.py
# ------------------------------

from kivy.uix.screenmanager import Screen


class DiagnosticScreen(Screen):
    def __init__(self, **kwargs):

        super(DiagnosticScreen, self).__init__(name='diagnosticscreen')

    def on_enter(self):

        """ call for a diagnostic scan at controller"""
        self.manager.controller.diagnostic_ui()

    def device_status(self, name, state, code):

        """ controller diagnostic ui sends information ragarding activated devices"""

        code = str(code)
        if name == 'coin_validator' and state == 'OK':

            self.ids._coin_img_status.source = 'images/green_ok.png'

        elif name == 'coin_validator' and state == 'Error':

            self.ids._coin_img_status.source = 'images/red_not_ok.png'
            self.ids._coin_lbl_status.text = "Coin validator status" + " Error / " + code

        if name == "ccTalk_communication" and state == "OK":
            self.ids._cctalk_img_status.source = "images/green_ok.png"

        elif name == "ccTalk_communication" and state == "Error":
            self.ids._cctalk_img_status.source = "images/red_not_ok.png"
            self.ids._cctalk_lbl_status.text = "ccTalk communication status" + " Error / " + code

        if name == "bill_validator" and state == "OK":
            self.ids._bill_img_status.source = "images/green_ok.png"

        elif name == "bill_validator" and state == "Error":
            self.ids._bill_img_status.source = "images/red_not_ok.png"
            self.ids._bill_lbl_status.text = "Bill validator status" + " Error / " + code

        if name == "hooper_status" and state == "OK":
            self.ids._hopper_img_status.source = "images/green_ok.png"

        elif name == "hooper_status" and state == "Error":
            self.ids._hopper_img_status.source = "images/red_not_ok.png"
            self.ids._hopper_lbl_status.text = "Hopper status" + " Error / " + code

        if name == "printer_status" and state == "OK":
            self.ids_printer_img_status.source = "images/green_ok"

        elif name == "printer_status" and state == "Error":
            self.ids_printer_img_status.source = "images/red_not_ok"
            self.ids._printer_lbl_status.text = "Printer status" + " Error / " + code
