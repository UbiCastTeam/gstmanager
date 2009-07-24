#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('detector')

class ParserBasedDetector(object):
    def __init__(self, file_path):
        self.file_path = file_path
        # TODO: regexp passing and parsing
        # Example with alsa: /proc/asound/devices

class FileBasedDetector(object):
    def __init__(self, file_pattern, type_desc):
        self.file_pattern = file_pattern
        self.type = type_desc
        self.devices_list = []

    def detect_devices(self):
        i = 0
        while True:
            file = "%s%s" %(self.file_pattern, i)
            import os
            if os.path.exists(file):
                logger.debug("Found %s device at %s" %(self.type, file))
                self.devices_list.append(file)
                i+=1
            else:
                logger.info("Found %s %s device(s)" %(len(self.devices_list),self.type))
                return self.devices_list
