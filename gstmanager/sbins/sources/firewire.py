#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.source import AVSource

class FirewireSource(AVSource):
    # Firewire Source class
    def __init__(self, device_id="0"):
        self.description = "Firewire source"
        self.type = "audio/video"
        sbin = "dv1394src port=%s" %device_id
        AVSource.__init__(self, sbin)
