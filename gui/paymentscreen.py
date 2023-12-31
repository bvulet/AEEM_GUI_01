# -------------------------------
# File name paymentscreen.py
# ------------------------------

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout


class PaymentScreen(Screen):
    def __init__(self, **kwargs):
        super(PaymentScreen, self).__init__(name='PaymentScreen')
        self.timer = None
        self.dismiss_pop_time = 5
        self.info_popup = Enpopup()
    def on_enter(self):
       return

    def inform_time(self, type, time_total):

        self.ids._time_description.text = str(type)
        self.ids._time_available.text = str(time_total)

    def amountinserted(self, inserted_amount, default_currency, converted_amount, other_currency):
        insert_to_screen = "{0}  {1}   {2}  {3}".format(inserted_amount, default_currency, converted_amount, other_currency)
        self.ids._amount_insert.text = str(insert_to_screen)



    def confirm_selection(self):
        """ on a press of a confirm function takes payment information selected and amount inserted
        based on thoose parameters calls a popoutselect function with information regarding the next steps,
        printer function if can and a hooper function that needs to return extra if needed. If yes, hooper function
        resets a counters, if not confirm button resets it because there is no need to return anything."""
        self.manager.controller.service_payment()

    def popoutselect(self, state):

        if state == "ok":

            the_content = Label(text="""Operation successful,\n 
                                    Please take your ticket!""", halign="left",
                                valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Confirmation', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()
        elif state == "unsufficient":
            the_content = Label(text="""Operation unsuccessful,\
                                        Please check your selection/payment\
                                        then try again or press !""", halign="left",
                                valign="top")

            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Operation unsuccessful!', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()
        elif state == "return":
            the_content = Label(text="""Operation successful,\
                                        Please take your ticket and rest of money!""", halign="left",
                                valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Confirmation', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()
        else:
            the_content = Label(text="""Operation unsuccessful,\
                                        Please check your selection, or insert money\
                                        In case of emergency press!""", halign="left",
                                valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Operation unsuccesful', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()
        Clock.schedule_once(popup.dismiss, self.dismiss_pop_time)

    def show_info_popup(self):
        self.info_popup.open()

    def write_owner_info(self, data):
        self.info_popup.write_popup_data(data)



class Enpopup(Popup):

    def __init__(self, **kwargs):
        super(Enpopup, self).__init__(**kwargs)
        self.dismiss_pop_time = 5

        Clock.schedule_once(self.dismiss_popup, self.dismiss_pop_time)

    def write_popup_data(self, data):
        self.ids._company_label.text = str(data['name'])
        self.ids._phone_label.text = str(data['phone'])
        self.ids._mail_label.text = str(data['mail'])


    def dismiss_popup(self, dt):
        self.dismiss()
