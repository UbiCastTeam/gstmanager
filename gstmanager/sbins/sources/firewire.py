#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.source import AVSource

class FirewireSource(AVSource):
    # Firewire Source class
    def __init__(self, device_id="0"):
        self.description = "Firewire source"
        self.type = "audio/video"
        a_caps = "audio/x-raw-int"
        v_caps = "video/x-raw-yuv, format=(fourcc)I420, width=(int)720, height=(int)576, framerate=(fraction)25/1, pixel-aspect-ratio=(fraction)1/1"
        sbin = "dv1394src port=%s ! queue ! dvdemux name=dv_src ! queue ! dvdec ! ffmpegcolorspace ! ffdeinterlace ! videoscale ! %s ! queue ! tee name=v_src_tee dv_src. ! %s ! queue ! tee name=a_src_tee" %(device_id, v_caps, a_caps)
        AVSource.__init__(self, sbin)
