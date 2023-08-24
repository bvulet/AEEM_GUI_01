# -----------------------------
# File name naplatascreen.py
# ----------------------------


from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout


class NaplataScreen(Screen):
    def __init__(self, **kwargs):

        super(NaplataScreen, self).__init__(name='NaplataScreen')
        self.info_popup = Dompopup()
        self.selected = None


    def on_enter(self):
        self.recognize_selected("None")
        self.manager.controller.check_reg_amount()
        return #povuci listu iz kontrolora za prikaz trenutnih cijena

    def inform_time(self, type, time_total):

        self.ids._time_description.text = str(type)
        self.ids._time_available.text = str(time_total)

    def amountinserted(self, inserted_amount, default_currency,converted_amount,other_currency):
        insert_to_screen = "{0}  {1}   {2}  {3}".format(inserted_amount, default_currency, converted_amount, other_currency)
        self.ids._amount_insert.text = str(insert_to_screen)

    def recognize_selected(self, product_type):
        self.selected = product_type
        self.manager.controller.check_selected_price(product_type)


    def confirm_selection(self):

        """ on a press of a confirm function takes payment information selected and amount inserted
        based on thoose parameters calls a popoutselect function with information regarding the next steps,
        printer function if can and a hooper function that needs to return extra if needed. If yes, hooper function
        resets a counters, if not confirm button resets it because there is no need to return anything."""
        if self.selected is None:
            self.popoutselect("not_selected")

        else:

            self.manager.controller.service_payment(self.selected)


    def popoutselect(self, state):

        if state == "ok":

            the_content = Label(text="""Uspješno ste izvršili transakciju,\n 
                                                Molimo preuzmite vašu kartu""", halign="left",
                                valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Potvrda o uspješnoj transakciji', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()
        elif state == "unsufficient":
            the_content = Label(text="""Neuspjela transakcija,\
                                        Molimo pregledajte svoj izbor,\
                                       zatim pokušajte iznova ili pritisnite !""", halign="left",
                                valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Neuspjela Transakcija!', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()
        elif state == "return":
            the_content = Label(text="""Uspješna transakcija,\
                                    Molimo preuzmite svoj ostatak novca!""", halign="left",
                                valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Potvrda o uspješnoj transakciji', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()
        else:
            the_content = Label(text="""Neuspjela akcija, unesite novac ili\
                                        pregledajte svoj izbor. Za slučaj greške pritisnite !
                                        """, halign="left", valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Neuspjela Transakcija!', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()
        Clock.schedule_once(popup.dismiss, 6)

    """ Namijenjeno da kada se pritisne confirm kaze ok placeno je obrada je u tijeku i printer ce 
    isprintati. ako nije dobar iznos kaze nije dobro nastavi nesto drugo"""

    def show_info_popup(self):

        self.info_popup.open()
    def write_owner_info(self, data):
        self.info_popup.write_popup_data(data)

        #self.ids._warningbtn.box_pop_label.text = str(data)

class Dompopup(Popup):

    def __init__(self, **kwargs):
        super(Dompopup, self).__init__(**kwargs)
        # call dismiss_popup in 4 seconds
        Clock.schedule_once(self.dismiss_popup, 4)


    def write_popup_data(self, data):
        self.ids._company_label.text= str(data['name'])
        self.ids._phone_label.text = str(data['phone'])
        self.ids._mail_label.text = str(data['mail'])


    def dismiss_popup(self, dt):
        self.dismiss()
