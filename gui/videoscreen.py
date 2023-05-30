# ------------------------------
# File name videoscreen.py
# ------------------------------


from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.video import Video


class VideoScreen(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(VideoScreen, self).__init__(name='videoscreen')
        self.video = None

    def create_video(self, directory):
        self.video = Video()

        self.video.options = {'eos': 'loop', 'allow_stretch': True}
        self.video.allow_stretch = True
        self.video.keep_ratio = False
        self.video.volume = 0
        self.video.source = directory
        self.ids._container.add_widget(self.video)

    def on_pre_enter(self, *args):
        self.video.state = 'play'

    def video_directory(self, directory):
        playlist = directory[0]
        if self.video is None:
            self.create_video(playlist)

        else:
            self.video.source = playlist
            self.video._trigger_video_load()

    def on_touch_down(self, touch):
        self.video.state = 'stop'
        self.manager.current = 'welcomescreen'
        return super(VideoScreen, self).on_touch_down(touch)

    def unload_video(self):

        self.video.unload()

    def load_video(self):
        pass

    def trigger_exit(self):
        if self.manager.current == 'videoscreen':
            self.video.state = 'stop'
            self.manager.current = 'welcomescreen'
        else:
            pass
