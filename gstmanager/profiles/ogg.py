
from gstmanager.profile import DefaultEncodingProfile

class OggDefaultRecordingProfile(DefaultEncodingProfile):
    def __init__(self):
        DefaultEncodingProfile.__init__(self)
        self.extension = "ogg"
        self.video_width = 320
        self.video_height = 240
        self.video_bitrate = 2000
        self.audio_bitrate = 128000
        self.video_quality = 16
        self.video_framerate = 25
