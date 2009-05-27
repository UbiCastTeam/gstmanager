#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
#os.environ['GST_DEBUG'] = '3'

import logging
import gst
from gstmanager.binmanager import BinManager
logger = logging.getLogger('shoutbin')

class ShoutBin(BinManager):
    # Bin for shoutcast/OGG video streaming
    def __init__(self, encoding_profile):
        BinManager.__init__(self, name="ShoutBin")

        self.profile = profile = encoding_profile

        self.vq0 = vq0 = self.add_element("queue")
        self.vproc = vproc = self.add_element("videoscale")
        self.vcol = vcol = self.add_element("ffmpegcolorspace")
        self.vcaps = vcaps = self.add_element("capsfilter")
        self.venc = venc = self.add_element("theoraenc")
        self.venc.set_properties("bitrate", profile.vbitrate) 
        self.vq1 = vq1 = self.add_element("queue")
        # leaky ?

        self.mux = mux = self.add_element("oggmux")
        #vpad = vpay.get_pad("src")
        #vpad.connect('notify::caps', self.notify_caps)

        self.sink = sink = self.add_element("shout2send")
        sink.set_property("ip", profile.ip)
        sink.set_property("port", profile.port)
        sink.set_property("username", profile.username)
        sink.set_property("password", profile.password)
        sink.set_property("mount", profile.mount)

        self.set_caps(vcaps, "video/x-raw-yuv, format=(fourcc)I420, framerate=(fraction)%s/1, width=(int)%s, height=(int)%s, pixel-aspect-ratio=(fraction)1/1" %(profile.framerate, profile.width, profile.height))

        vq0.link(vproc)
        vproc.link(vcol)
        vcol.link(vcaps)
        vcaps.link(venc)
        venc.link(vq1)
        vq1.link(mux)
        mux.link(sink)
        
        vinput_pad = vq0.get_pad("sink")
        self.add_ghostpad_from_static("vinput", vinput_pad)

        self.aq0 = aq0 = self.add_element("queue")
        self.aconv = aconv = self.add_element("audioconvert")
        self.aenc = aenc = self.add_element("vorbisenc")
        aenc.set_property("bitrate", profile.abitrate)
        self.aq1 = aq1 = self.add_element("queue")

        aq0.link(aconv)
        aconv.link(aenc)
        aenc.link(aq1)
        aq1.link(mux)

        ainput_pad = aq0.get_pad("sink")
        self.add_ghostpad_from_static("ainput", ainput_pad)
