#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gst
from gstmanager.binmanager import BinManager

class FirewireBin(BinManager):
    def __init__(self):
        BinManager.__init__(self, name="FirewireBin")
        self.src = src = self.add_element("dv1394src")
        self.demux = demux = self.add_element("dvdemux")
        vspad = demux.get_pad("video")

        vdec = self.add_element("dvdec")
        vdpad = vdec.get_pad("sink")
        vspad.link(vdpad)

        voutput_pad = vdec.get_pad("src")
        self.add_ghostpad_from_static("voutput", voutput_pad)

        aoutput_pad = demux.get_pad("audio")
        self.add_ghostpad_from_static("aoutput", aoutput_pad)
