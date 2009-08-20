#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.source import VideoSource, AudioSource

class DVVideoSource(VideoSource):
    def __init__(self, device_id="0"):
        self.description = "Video DV (Firewire) source"
        self.type = "video"
        v_caps = "video/x-raw-yuv, format=(fourcc)I420, width=(int)720, height=(int)576, framerate=(fraction)25/1, pixel-aspect-ratio=(fraction)1/1"
        sbin = "dv1394src port=%s ! queue ! dvdemux name=dv_src ! queue ! dvdec ! ffmpegcolorspace ! ffdeinterlace ! videoscale ! %s" %(device_id, v_caps)
        VideoSource.__init__(self, sbin)

class DVAudioSource(AudioSource):
    def __init__(self):
        self.description = "Audio DV (Firewire) source"
        self.type = "audio"
        a_caps = "audio/x-raw-int"
        sbin = "dv_src. ! %s" %a_caps
        AudioSource.__init__(self, sbin)
