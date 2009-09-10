#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.encoder import VideoEncoder, AudioEncoder
from gstmanager.sbins.muxer import Muxer

class TheoraEncoder(VideoEncoder):
    def __init__(self, profile):
        self.description = "Theora encoder"
        self.type = "video"
        sbin = "theoraenc bitrate=%s quality=%s" %(profile.video_bitrate, profile.video_quality)
        VideoEncoder.__init__(self, sbin, profile=profile)

class VorbisEncoder(AudioEncoder):
    def __init__(self, profile):
        self.description = "Vorbis encoder"
        self.type = "audio"
        sbin = "vorbisenc bitrate=%s" %profile.audio_bitrate
        AudioEncoder.__init__(self, sbin)

class OggMuxer(Muxer):
    def __init__(self):
        self.description = "Ogg Muxer"
        self.type = "audio/video"
        sbin = "oggmux"
        Muxer.__init__(self, sbin)

from gstmanager.sbins.encoder import FileEncoder
from gstmanager.profile import DefaultEncodingProfile

class OggEncoder(FileEncoder):
    def __init__(self, filename="/tmp/test.ogg",profile=DefaultEncodingProfile()):
        filename = "%s.%s" %(filename, profile.extension)
        FileEncoder.__init__(self, filename)


        self.venc = TheoraEncoder(profile)
        self.aenc = VorbisEncoder(profile)
        self.muxer = OggMuxer()
        self.add(self.venc)
        self.add(self.aenc)
        self.add(self.muxer)
        self.tags = ["a_src", "v_src"]
        self.type = "audio-video"
        self.description = "Ogg to File Encoder"
        self.sbin = "%s muxer_tee. ! filesink location=%s" %(self.pipeline_desc, filename)
