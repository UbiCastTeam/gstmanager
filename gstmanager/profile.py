#!/usr/bin/env python
# -*- coding: utf-8 -*-

from event import EventLauncher, EventListener

class DefaultEncodingProfile(EventLauncher, EventListener):
    def __init__(self):
        EventLauncher.__init__(self)
        EventListener.__init__(self)
        # In kbits/s
        self.video_bitrate = vb = 2000 
        # In bits/s
        self.audio_bitrate = ab = 128000
        # In kbits/s
        self.video_width = 320 
        self.video_height = 240
        self.video_framerate = 25
        self.registerEvent("sos")

    def get_string(self):
        return self.__dict__

    def get_total_bitrate(self):
        total_bitrate = self.video_bitrate + self.audio_bitrate/1000
        return total_bitrate
