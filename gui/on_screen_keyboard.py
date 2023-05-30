
# ostat ce do razvoja, ovo spremiti negdje i ne ide u aplikaciju


from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.widget import Widget

class On_Screen_Keyboard ():
    def __init__(self, **kwargs):
        self.set_layouts()
        self._keyboard = None
        self.label_id = None




    def set_layouts(self):
        layouts = list(VKeyboard().available_layouts.keys())
        layouts.append("numeric.json")


    def add_keyboards(self, layout):


        keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')

        if keyboard.widget:
            self._keyboard = keyboard.widget
            self._keyboard.layout = layout

        else:
            self._keyboard = keyboard

        self._keyboard.bind(on_key_down= self.key_up,
                            on_key_up = self._on_keyboard_up)




    def _keyboard_closed(self):

        if self._keyboard:
            self._keyboard.unbind(on_key_down= self.key_up)
            self._keyboard.unbind(on_key_up= self._on_keyboard_up)
            self._keyboard = None


    def _on_keyboard_up(self, keyboard, keycode, text, modifiers):

        index = list(self.ids.values()).index(self.label_id)
        widget_ids = list(self.ids.keys())
        local_id = widget_ids[index]

        if isinstance(keycode, tuple):

            keycode = keycode[1]

        # Keycode is composed of an integer + a string
        #If we hit escape, release the keyboard
        if keycode =='backspace':
            if local_id == "_username":
                temp_text = self.ids._username.text
                temp_text=temp_text[:-1]
                self.ids._username.text = temp_text
                keycode =''

            elif local_id =="_password":
                temp_text = self.ids._password.text
                temp_text = temp_text[:-1]
                self.ids._password.text = temp_text
                keycode = ''




        if keycode == 'escape':
            print("escape je prihvacen")
            print("self keyboard je", self._keyboard)
            Window.release_keyboard()

        #Return True to accept the key. Otherwise, it will be used by
        #the system.
        return True



    def key_up(self, *args):
        print("idemoo")
