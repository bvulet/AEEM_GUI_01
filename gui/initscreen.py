# -------------------------------
# File name initscreen.py
# ------------------------------

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class InitScreen(Screen):
    def __init__(self, **kwargs):

        super(InitScreen, self).__init__(name='initscreen')
        self.w_start_angle = 90
        self.w_end_angle = 360
        self.set_events = None
        self.inital_procedure = None
        self.counter = 0

    def on_enter(self):
        self.animation_show()

    def on_pre_leave(self, *args):
        self.exit_animation_show()
        self.manager.controller.video_start_state(True)
        self.manager.controller.start_devices()

    def animation_show(self):
        self.inital_procedure = True
        self.ids._welcome_icon.source = "images/logo_01.png"
        self.set_events = Clock.schedule_interval(self.animate, .3)

    def animate(self, *args):
        if self.counter%2:
            self.ids._welcome_icon.source = "images/logo_02.png"

        else:
            self.ids._welcome_icon.source = "images/logo_01.png"
        self.counter += 1
        self.w_start_angle += 20
        self.w_end_angle += 20
        self.ids._init_line._angle_start_internal = self.w_start_angle
        self.ids._init_line._angle_end_internal = self.w_end_angle

    def exit_animation_show(self):

        self.inital_procedure = False

        self.set_events.cancel()
