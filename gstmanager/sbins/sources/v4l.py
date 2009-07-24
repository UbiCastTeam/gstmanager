#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.source import Source

class V4LSource(Source):
    # V4L Source class
    def __init__(self, device_id="/dev/video0"):
        Source.__init__(self)
        self.description = "V4L source"
        self.type = "video"
        self.sbin = "v4lsrc name=%s device=%s" %(self.tag, device_id)
