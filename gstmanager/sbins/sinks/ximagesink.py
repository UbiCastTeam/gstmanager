#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.sink import VideoSink

class XImageSink(VideoSink):
    # X Image Sink class
    def __init__(self): 
        VideoSink.__init__(self)
        self.description = "X Image Sink"
        self.type = "video"
        self.sbin = "ximagesink name=%s" %self.tag
