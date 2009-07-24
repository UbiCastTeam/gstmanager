#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.source import Source

class VideoTestSource(Source):
    # Video Test Source class
    def __init__(self, device_id="0"):
        Source.__init__(self)
        self.description = "Video Test Source"
        self.type = "video"
        self.sbin = "videotestsrc name=%s pattern=%s" %(self.tag, device_id)
