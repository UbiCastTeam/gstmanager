#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DefaultEncodingProfile(object):
    def __init__(self):
        self.video_bitrate = 2000 
        self.audio_bitrate = 128000 
        self.video_width = 320 
        self.video_height = 240 

    def get_string(self):
        return self.__dict__
