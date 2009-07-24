#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.source import Source

class AudioTestSource(Source):
    # Alsa Source class
    def __init__(self):
        Source.__init__(self)
        self.description = "Audio test source"
        self.type = "audio"
        self.sbin = "audiotestsrc name=%s" %self.tag
