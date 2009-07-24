#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.source import Source

class FirewireSource(Source):
    # Firewire Source class
    def __init__(self, device_id="0"):
        Source.__init__(self)
        self.description = "Firewire source"
        self.type = "audio/video"
        self.sbin = "dv1394src name=%s port=%s" %(self.tag, device_id)
