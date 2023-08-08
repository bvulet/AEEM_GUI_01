# -------------------------------
# File name usercontrolscreen.py
# ------------------------------

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from on_screen_keyboard import On_Screen_Keyboard
from kivy.uix.textinput import TextInput
from kivy.uix.vkeyboard import VKeyboard
from kivy.core.window import Window


class UsercontrolScreen(Screen, On_Screen_Keyboard):
    def __init__(self, **kwargs):
        self.pop_dismiss_time = 6
        super(UsercontrolScreen, self).__init__(name='usercontrolscreen')

    def change_password(self, id_sel, password):
        index = list(self.ids.values()).index(id_sel)
        widget_ids = list(self.ids.keys())
        local_id = widget_ids[index]
        self.manager.user_accounts.change_user_passwords(local_id, password)

    def reset_text_input(self):

        self.ids._old_diag_pass.text = ""
        self.ids._old_dev_pass.text = ""

    def popoutselect(self, state, id_sel):

        if state == "ok":

            the_content = Label(text="""Uspješno ste promijenili šifru za\n""" + id_sel, halign="left",
                                valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Potvrda o uspješnoj akciji', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()
        elif state == "req_error":
            the_content = Label(text="Dužina šifre manja of 4 znamenke ili ne sadrži veliko slovo !",
                                halign="left", valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Neuspjela akcija!', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()

        else:
            the_content = Label(text="""Neuspjela akcija, molimo vratite se\n
                                           u početni zaslon i probajte iznova !""",
                                halign="left", valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Neuspjela Transakcija!', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()
        Clock.schedule_once(popup.dismiss, self.pop_dismiss_time)


class PasswordInput(TextInput):

    def __init__(self, **kwargs):
        super(PasswordInput, self).__init__(**kwargs)
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
