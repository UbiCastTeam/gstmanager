#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gst
from gstmanager.binmanager import BinManager

class TestSrcBin(BinManager):
    def __init__(self):
        BinManager.__init__(self, name="TestSrcBin")
        self.vsrc = vsrc = self.add_element("videotestsrc")
        self.ascr = asrc = self.add_element("audiotestsrc")

        voutput_pad = vsrc.get_pad("src")
        self.add_ghostpad_from_static("voutput", voutput_pad)

        aoutput_pad = asrc.get_pad("src")
        self.add_ghostpad_from_static("aoutput", aoutput_pad)
