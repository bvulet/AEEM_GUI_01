# ------------------------------
# File name videocontrolscreen.py
# ------------------------------


from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


class VideoControlScreen(Screen, FloatLayout):
    def __init__(self, **kwargs):

        super(VideoControlScreen, self).__init__(name='videocontrolscreen')
        self.video_permit = True
        self.button_color_red = 255, 0, 0, 1
        self.button_color_gray = 1, 1, 1, 1
        self.destination_directory = None
        self.external_directory = None
        self.filechooser1 = None
        self.filechooser2 = None
        self.copy_file = None
        self.popup_dismiss = 2

    def start_filechooser(self, directory, usb_directorys):

        self.filechooser1 = FileChooserIconView()
        self.filechooser1.id = "filechooser1"
        self.filechooser1.rootpath = usb_directorys

        self.filechooser1.selection = []
        self.ids._box_container.add_widget(self.filechooser1)

        self.filechooser2 = FileChooserIconView()
        self.filechooser2.id = "filechooser2"
        self.filechooser2.path = directory
        self.destination_directory = directory
        self.filechooser2.selection = []
        self.ids._box_container.add_widget(self.filechooser2)

    def video_permission(self):

        self.manager.controller.video_control_and_permission()
        self.video_permit = False

    def inform_video_user(self, state):

        if state:
            self.ids._video_button_control.text = "Disable video"
            self.ids._video_button_control.background_color = self.button_color_gray

        else:
            self.ids._video_button_control.text = "Enable video"
            self.ids._video_button_control.background_color = self.button_color_red

    # def check_destination_folder(self):
    def on_enter(self):

        self.manager.controller.video_start_state(False)
        self.manager.controller.unload_video_file()

    def destination_folder_connect(self, directory, usb_directorys):

        self.destination_directory = directory
        self.external_directory = usb_directorys

        if self.filechooser1 is None and self.filechooser2 is None:

            self.start_filechooser(directory, usb_directorys)
        else:
            self.manage_filechooser(directory, usb_directorys)

    def manage_filechooser(self, directory, usb_directorys):

        self.filechooser1.rootpath = usb_directorys
        self.filechooser2.rootpath = directory

        self.filechooser1._update_files()
        self.filechooser1._update_item_selection()
        self.filechooser1.selection = []
        self.filechooser2._update_files()
        self.filechooser2._update_item_selection()
        self.filechooser2.selection = []

    def copy_selected(self):

        if len(self.filechooser1.selection) == 0:
            self.inform_user(0)

        else:
            self.copy_file = self.filechooser1.selection[0]
            self.filechooser1.selection = []

    def paste_selected(self):

        self.manager.controller.save_folder_managing(self.copy_file,
                                                     self.destination_directory)

    def delete_video(self):
        if len(self.filechooser2.selection) == 0:
            self.inform_user(0)

        else:

            delete_file = self.filechooser2.selection[0]
            self.manager.controller.delete_folder_managing(delete_file)

    def inform_user(self, state):

        if state == 0:

            the_content = Label(text="""Nije odabrana datoteka!""", halign="left",
                                valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Upozorenje!', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()

        elif state == 1:
            the_content = Label(text="""Uspješna akcija!""", halign="left",
                                valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Potvrda!', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()

        elif state == 2:
            the_content = Label(text="""Greška u radu molimo napustite akciju!""", halign="left",
                                valign="top")
            the_content.bind(size=lambda s, w: s.setter('text_size')(s, w))
            the_content.color = (1, 1, 1, 1)
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(the_content)
            popup = Popup(title='Upozorenje!', title_size=20,
                          content=box_layout, size_hint=(None, None),
                          size=(350, 150))
            popup.open()

        self.filechooser1._update_files()
        self.filechooser2._update_files()
        Clock.schedule_once(popup.dismiss, self.popup_dismiss)

    # def inform_video_update(self):
    def on_leave(self, *args):

        self.manager.controller.update_video_playlist(self.destination_directory)
