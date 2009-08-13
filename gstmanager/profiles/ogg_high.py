
from gstmanager.profile import DefaultEncodingProfile

class OggRecordingProfile(DefaultEncodingProfile):
    def __init__(self):
        DefaultEncodingProfile.__init__(self)
        self.extension = "ogg"
        self.video_width = 512
        self.video_height = 384
        self.video_bitrate = 3000
        self.audio_bitrate = 128000
