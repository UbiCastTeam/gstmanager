#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.sources.dv import DVVideoSource
from gstmanager.sbins.encoder import FileEncoder

from gstmanager.profiles.dv import DefaultDVProfile

class DVDumper(FileEncoder):
    def __init__(self, device_id="0", filename="/tmp/test", profile=DefaultDVProfile()):
        filename = "%s.%s" %(filename, profile.extension)
        FileEncoder.__init__(self, filename)
        self.profile = profile
        self.enc = DVVideoSource(device_id=device_id, filename=filename)
        self.add(self.enc)
        self.tags = ["dv_src"]
        self.type = "audio-video"
        self.description = "DV Source File Dumper"
        self.sbin = self.pipeline_desc
