# -------------------------------
# File name loginscreen.py
# ------------------------------


from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput


class LoginScreen(Screen, Widget):
    _username = ObjectProperty()
    _password = ObjectProperty()

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(name='loginscreen')
        self.dev_pass = None
        self.dev_user = None
        self.video_user = None
        self.diag_user = None
        self.diag_pass = None
        self.diag_master_pass = None
        self.diag_master_user = None
        self.dev_master_pass = None
        self.dev_master_user = None
        self.video_master_user = None
        self.video_pass = None
        self.video_master_pass = None

    def account_setup(self, dev_user, dev_pass, diag_user, diag_pass, video_user, video_pass):
        self.dev_user = dev_user
        self.dev_pass = dev_pass
        self.diag_user = diag_user
        self.diag_pass = diag_pass
        self.video_user = video_user
        self.video_pass = video_pass

    def master_account_setup(self, master_dev_user, master_dev_pass, master_diag_user,
                             master_diag_pass, master_video_user, master_video_pass):
        self.dev_master_user = master_dev_user
        self.dev_master_pass = master_dev_pass
        self.diag_master_user = master_diag_user
        self.diag_master_pass = master_diag_pass
        self.video_master_user = master_video_user
        self.video_master_pass = master_video_pass

    def do_login(self, username, password):

        username = str(username)
        password = str(password)
        if username == self.diag_master_user:
            print(username, self.diag_master_user)
        if password == self.diag_master_pass:
            print(password, self.diag_master_pass)
        if (username == self.diag_user or username == self.diag_master_user) and \
                (password == self.diag_pass or password == self.diag_master_pass):

            self.manager.current = 'diagnosticscreen'
            self.ids._error_label.color = 0, 0, 0, 0
            self.ids._username.text = ""
            self.ids._password.text = ""

        elif (username == self.dev_user or username == self.dev_master_user) \
                and (password == self.dev_pass or password == self.dev_master_pass):
            self.manager.current = 'developerscreen'
            self.ids._error_label.color = 0, 0, 0, 0
            self.ids._username.text = ""
            self.ids._password.text = ""

        elif (username == self.video_user or username == self.video_master_user) \
                and (password == self.video_pass or password == self.video_master_pass):
            self.manager.current = 'videocontrolscreen'
            self.ids._error_label.color = 0, 0, 0, 0
            self.ids._username.text = ""
            self.ids._password.text = ""

        else:
            self.ids._error_label.color = 1, 1, 1, 1
            self.ids._password.text = ""


# ---------------------------------------------------------------
# s obzirom da tipkovnica zaista nije rijesena bas nesto
# ekstra ostavljam ovaj dio ako bi se bilo pametnije u buducnosti
# -----------------------------------------------------------------
class CustomTextInput(TextInput):

    def __init__(self, **kwargs):

        super(CustomTextInput, self).__init__(**kwargs)
        self.set_layouts()
        self.layouts = None
        self.keyboard = None
        self.kb = None

    def set_layouts(self):

        self.layouts = list(VKeyboard().available_layouts.keys())
        self.layouts.append("numeric.json")

    def on_focus(self, instance, value):

        self.set_layouts()
        self._ensure_keyboard()
        keyboard = self._get_keyboard()
        layouts = self.layouts
        if keyboard.widget:
            self.kb = keyboard.widget
            self.kb.layout = 'qwerty'

        else:
            self.kb = keyboard

    def exit_screen(self):

        self.focus = False
        Window.release_all_keyboards()
