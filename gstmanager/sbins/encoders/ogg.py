#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.encoder import VideoEncoder, AudioEncoder
from gstmanager.sbins.muxer import Muxer

class TheoraEncoder(VideoEncoder):
    def __init__(self):
        self.description = "Theora encoder"
        self.type = "video"
        sbin = "theoraenc bitrate=2000"
        VideoEncoder.__init__(self, sbin)

class VorbisEncoder(AudioEncoder):
    def __init__(self):
        self.description = "Vorbis encoder"
        self.type = "audio"
        sbin = "vorbisenc bitrate=128000"
        AudioEncoder.__init__(self, sbin)

class OggMuxer(Muxer):
    def __init__(self):
        self.description = "Ogg Muxer"
        self.type = "audio/video"
        sbin = "oggmux"
        Muxer.__init__(self, sbin)

from gstmanager.sbinmanager import SBinManager

class OggEncoder(SBinManager):
    def __init__(self, filename):
        SBinManager.__init__(self)
        self.check_for_compat = False
        self.venc = TheoraEncoder()
        self.aenc = VorbisEncoder()
        self.muxer = OggMuxer()
        self.add(self.venc)
        self.add(self.aenc)
        self.add(self.muxer)
        self.tags = ["a_src", "v_src"]
        self.type = "audio-video"
        self.description = "Ogg to File Encoder"
        self.filename = filename
        self.sbin = "%s muxer_tee. ! filesink location=%s" %(self.pipeline_desc, filename)

    def get_file(self):
        return self.filename
