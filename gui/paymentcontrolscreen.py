# -------------------------------
# File name paymentcontrolscreen.py
# ------------------------------

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.vkeyboard import VKeyboard
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class PaymentControlScreen(Screen):

    def __init__(self, **kwargs):

        super(PaymentControlScreen, self).__init__(name='paymentcontrolscreen')
        self.disable_req = None
        self.image_ok = "images/green_ok.png"
        self.image_not_ok = "images/red_not_ok.png"
        self.button_color_red = 255, 0, 0, 1
        self.button_color_gray = 1, 1, 1, 1
        self.popout_dismiss_time = 6

    def on_pre_enter(self, *args):
        self.manager.controller.read_device_parameters()
        self.manager.controller.check_prices()




    def show_old_prices(self, value, currency):

        self.ids._currency_label_1.text = currency
        self.ids._currency_label_2.text = currency
        self.ids._currency_label_3.text = currency
        self.ids._currency_label_4.text = currency
        self.ids._reg_price_1.text = str(value[0])
        self.ids._reg_price_2.text = str(value[1])
        self.ids._action_price_1.text = str(value[2])
        self.ids._action_price_2.text = str(value[3])


    def request_new_prices(self, section, id, value):
        constant = 0.5
        #index = list(self.ids.values()).index(id)
       # widget_ids = list(self.ids.keys())
       # local_id = widget_ids[index]

        if value == "" or "insert" in value:
            self.popoutselect('empty', id)
            pass
        elif float(value) % constant:
            self.popoutselect('price_error', id)

        else:
            price = float(value)
            self.manager.controller.price_set(section, id, price)

    def disable_devices(self, section, device):

        self.disable_req = device
        self.manager.controller.device_control(section, device)

    def inform_screen(self, req_type):

        if req_type == "dual_currency_enable":
            self.ids._dual_currency_light.source = self.image_ok
            self.ids._dual_currency_button.background_color = self.button_color_gray

        if req_type == "dual_currency_disable":
            self.ids._dual_currency_light.source = self.image_not_ok
            self.ids._dual_currency_button.background_color = self.button_color_red

        if req_type == "payment_enable":
            self.ids._payment_light.source = self.image_ok
            self.ids._payment_button.background_color =  self.button_color_gray


        if req_type == "payment_disable":
            self.ids._payment_light.source = self.image_not_ok
            self.ids._payment_button.background_color = self.button_color_red

        if req_type == "action_price_1_active":
            self.ids._action_price_1_light.source = self.image_ok
            self.ids._action_price_1_button.background_color =  self.button_color_gray

        if req_type == "action_price_1_disable":
            self.ids._action_price_1_light.source = self.image_not_ok
            self.ids._action_price_1_button.background_color = self.button_color_red

        if req_type == "action_price_2_active":
            self.ids._action_price_2_light.source = self.image_ok
            self.ids._action_price_2_button.background_color =  self.button_color_gray

        if req_type == "action_price_2_disable":
            self.ids._action_price_2_light.source = self.image_not_ok
            self.ids._action_price_2_button.background_color = self.button_color_red




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
