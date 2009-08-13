#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.source import VideoSource

class V4LSource(VideoSource):
    # V4L Source class
    def __init__(self, device_id="/dev/video0", v4l_version=None):
        self.description = "V4L source"
        self.type = "video"
        sbin = "v4l%ssrc device=%s" %(v4l_version, device_id)
        VideoSource.__init__(self, sbin)
