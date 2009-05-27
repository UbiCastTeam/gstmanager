#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gst
from gstmanager.binmanager import BinManager

class AlsaV4LBin(BinManager):
    def __init__(self):
        BinManager.__init__(self, name="AlsaV4LBin")
        self.vsrc = vsrc = self.add_element("v4lsrc")
        self.ascr = asrc = self.add_element("alsasrc")

        voutput_pad = vsrc.get_pad("src")
        self.add_ghostpad_from_static("voutput", voutput_pad)

        aoutput_pad = asrc.get_pad("src")
        self.add_ghostpad_from_static("aoutput", aoutput_pad)
