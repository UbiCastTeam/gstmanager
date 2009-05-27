#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DefaultStreamingProfile:
    def __init__(self):
        self.desc = "Base RTP Streaming profile"
        self.framerate = 30
        self.width = 480
        self.height = 384
        self.vbitrate = 1000
        self.abitrate = 128000
        self.ip = "127.0.0.1"
        self.vport = 10000
        self.aport = 10002

    def to_string(self):
        print "%s: Framerate: %s fps, Width: %s, Height: %s, VBitrate: %s, ABitrate: %s, IP: %s, VPort: %s, APort: %s" %(self.desc, self.framerate, self.width, self.height, self.vbitrate, self.abitrate, self.ip, self.vport, self.aport)
