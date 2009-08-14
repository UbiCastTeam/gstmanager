#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.source import AudioSource

class AlsaSource(AudioSource):
    def __init__(self, device_id="0"):
        self.description = "Alsa source"
        self.type = "audio"
        sbin = "alsasrc device=hw:%s,0 latency-time=300000" %device_id
        AudioSource.__init__(self, sbin)
