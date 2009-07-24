#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.detector import FileBasedDetector

class FirewireDetector(FileBasedDetector):
    def __init__(self):
        FileBasedDetector.__init__(self, "/dev/dv1394/", "Firewire card")

    def detect_devices(self):
        super(FirewireDetector, self).detect_devices()
        self.devices_list = [device[12:] for device in self.devices_list]
