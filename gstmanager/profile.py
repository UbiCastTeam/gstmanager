#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DefaultEncodingProfile:
    def __init__(self):
        self.video_bitrate = 2000 
        self.audio_bitrate = 128000 
        self.video_width = 320 
        self.video_height = 240 
        self.server = "127.0.0.1"
        self.video_port = "1234" 
        self.audio_port = "1235" 
        self.encoding_threads = "2"
