# ------------------------------
# File name welcomescreen.py
# ------------------------------

from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


class WelcomeScreen(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(name='welcomescreen')
        self.ids._logoadvanced.source = 'images/logo_01.png'
        self.screen_permission = True
        self.counter = 0
        self.video_permission = True
        self.set_timer = None
        self.time_duration = 10
        self.set_events = None

    def on_enter(self):
        self.start_lang_animation()
        self.trigger_video()

    def on_leave(self, *args):
        self.exit_anim_screen()

    def enter_image_screen(self):

        self.ids._logoadvanced.source = 'images/logo_02.png'

    def exit_image(self):

        self.ids._logoadvanced.source = 'images/logo_01.png'

    def detect_hr_press(self):

        if self.screen_permission:

            self.manager.current = 'naplatascreen'

        else:
            pass

        self.ids._welcome_hr_image.source = 'images/bih_p_01.png'

    def detect_hr_release(self):
        self.ids._welcome_hr_image.source = 'images/bih_png.png'

    def detect_int_press(self):
        if self.screen_permission:
            self.manager.current = 'paymentscreen'

        else:
            pass
        self.ids._welcome_int_image.source = 'images/international_p_01.png'

    def detect_int_release(self):

        self.ids._welcome_int_image.source = 'images/world.png'

    def disable_ui_device(self, permission):
        # stoji ovdje medutim nema smisla to raditi ako ga mozemo ugasiti iz struje i kraj
        pass

    def start_lang_animation(self):
        self.set_events = Clock.schedule_interval(self.animate, .5)
        self.animate()

    def animate(self, *args):

        if not self.counter % 2:

            self.ids._welcome_layout._anim_color = (.1, 1, .1, .9)
            self.counter += 1

        else:

            self.ids._welcome_layout._anim_color = (.9, 9, .9, 1)
            self.counter = 0

    def trigger_video(self):
        if self.video_permission and self.manager.current == 'welcomescreen':

            self.set_timer = Clock.create_trigger(self.count_time, self.time_duration)
            self.set_timer()
        else:
            pass

    def on_touch_down(self, touch):
        if self.video_permission and self.manager.current == 'welcomescreen':
            if self.set_timer is not None:
                # reset the timer
                Clock.unschedule(self.count_time)

            if self.manager.current == 'welcomescreen':
                self.set_timer()

        else:
            pass
        return super(WelcomeScreen, self).on_touch_down(touch)

    def exit_anim_screen(self, *args):

        # cancel the  video timer
        if self.video_permission:
            Clock.unschedule(self.count_time)

        self.counter = 0
        self.ids._welcome_layout._anim_color = (1, 1, 1, 1)
        Clock.unschedule(self.animate)

    def count_time(self, *args):

        self.manager.current = 'videoscreen'

    def video_permission_control(self, status):

        self.video_permission = status
