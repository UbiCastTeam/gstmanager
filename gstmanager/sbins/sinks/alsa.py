#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.sink import AudioSink

class AlsaSink(AudioSink):
    def __init__(self, sync=True): 
        self.description = "Alsa audio sink"
        self.type = "audio"
        sbin = "alsasink sync=%s" %sync
        AudioSink.__init__(self, sbin)
