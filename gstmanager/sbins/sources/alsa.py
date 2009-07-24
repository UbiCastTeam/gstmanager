#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.source import Source

class AlsaSource(Source):
    # Alsa Source class
    def __init__(self, device_id="0"):
        Source.__init__(self)
        self.description = "Alsa source"
        self.type = "audio"
        self.sbin = "alsasrc name=%s device=hw:%s,0" %(self.tag, device_id)
