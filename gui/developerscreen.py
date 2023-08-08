# -------------------------------
# File name developerscreen.py
# ------------------------------

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.vkeyboard import VKeyboard
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class DeveloperScreen(Screen):

    def __init__(self, **kwargs):

        super(DeveloperScreen, self).__init__(name='developerscreen')
        self.disable_req = None
        self.image_ok = "images/green_ok.png"
        self.image_not_ok = "images/red_not_ok.png"
        self.button_color_red = 255, 0, 0, 1
        self.button_color_gray = 1, 1, 1, 1
        self.popout_dismiss_time = 6

    def on_pre_enter(self, *args):
        self.manager.controller.read_device_parameters()
        self.manager.controller.check_price_options()


    # def request_old_prices(self):
    #     self.manager.controller.read_device_parameters()





    #     self.manager.controller.check_prices()

    def show_old_prices(self, id, value, currency):

        blank = " "
        self.ids._15_min_price_label.text = str(value[0]) + blank + currency
        self.ids._30_min_price_label.text = str(value[1]) + blank + currency
        self.ids._45_min_price_label.text = str(value[2]) + blank + currency
        self.ids._1_h_price_label.text = str(value[3]) + blank + currency
        self.ids._2_h_price_label.text = str(value[4]) + blank + currency
        self.ids._24_h_price_label.text = str(value[5]) + blank + currency

    def request_new_prices(self, id, value):
        constant = 0.5
        index = list(self.ids.values()).index(id)
        widget_ids = list(self.ids.keys())
        local_id = widget_ids[index]

        if value == "" or "insert" in value:
            self.popoutselect('empty', local_id)
            pass
        elif float(value) % constant:
            self.popoutselect('price_error', local_id)

        else:
            price = float(value)
            self.manager.controller.price_set(local_id, price)

    def disable_devices(self, device):

        self.disable_req = device
        self.manager.controller.device_check(device)

    def inform_disable(self, req_type):

        if req_type == "all_disabled":
            self.ids._all_device_disabled_light.source = self.image_not_ok
            self.ids._all_device_disable_button.background_color = self.button_color_red
            self.ids._coin_device_disabled_light.source = self.image_not_ok
            self.ids._coin_device_disable_button.background_color = self.button_color_red
            self.ids._bill_device_disabled_light.source = self.image_not_ok
            self.ids._bill_device_disable_button.background_color = self.button_color_red
            self.ids._hooper_device_disabled_light.source = self.image_not_ok
            self.ids._hooper_device_disable_button.background_color = self.button_color_red

        elif req_type == "all_enabled":
            self.ids._all_device_disabled_light.source = self.image_ok
            self.ids._all_device_disable_button.background_color = self.button_color_gray
            self.ids._coin_device_disabled_light.source = self.image_ok
            self.ids._coin_device_disable_button.background_color = self.button_color_gray
            self.ids._bill_device_disabled_light.source = self.image_ok
            self.ids._bill_device_disable_button.background_color = self.button_color_gray
            self.ids._hooper_device_disabled_light.source = self.image_ok
            self.ids._hooper_device_disable_button.background_color = self.button_color_gray

        elif req_type == "coin_disable":
            self.ids._coin_device_disabled_light.source = self.image_not_ok
            self.ids._coin_device_disable_button.background_color = self.button_color_red

        elif req_type == "coin_enable":
            self.ids._coin_device_disabled_light.source = self.image_ok
            self.ids._coin_device_disable_button.background_color = self.button_color_gray

        elif req_type == "bill_enable":
            self.ids._bill_device_disabled_light.source = self.image_ok
            self.ids._bill_device_disable_button.background_color = self.button_color_gray

        elif req_type == "bill_disable":
            self.ids._bill_device_disabled_light.source = self.image_not_ok
            self.ids._bill_device_disable_button.background_color = self.button_color_red

        elif req_type == "hooper_enable":
            self.ids._hooper_device_disabled_light.source = self.image_ok
            self.ids._hooper_device_disable_button.background_color = self.button_color_gray

        elif req_type == "hooper_disable":
            self.ids._hooper_device_disabled_light.source = self.image_not_ok
            self.ids._hooper_device_disable_button.background_color = self.button_color_red

        elif req_type == "req_error":
            # upisi tekst da je greska u obradi zahtjeva

            pass
        elif req_type == "unexpected_err":
            # upisi na welcome screen nesto pitanje je ide li ovamo to uopce
            pass

    def popoutselect(self, state, id):

        if state == "empty":

            the_content = Label(text="""Unesite cijenu za\n""" + id, halign="left",
                                valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Neuspjela akcija', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()
            Clock.schedule_once(popup.dismiss, self.popout_dismiss_time)
        elif state == "price_error":
            the_content = Label(text="Cijena mora biti u koracima 0,5,1,1.5,2... !",
                                halign="left", valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Neuspjela akcija!', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()
            Clock.schedule_once(popup.dismiss, self.popout_dismiss_time)


class PriceInput(TextInput):

    def __init__(self, **kwargs):

        super(PriceInput, self).__init__(**kwargs)
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
            self.kb.layout = 'numeric.json'

        else:
            self.kb = keyboard

    def exit_screen(self):

        self.focus = False
        Window.release_all_keyboards()
