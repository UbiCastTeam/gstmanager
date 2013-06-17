#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.encoder import VideoEncoder
from gstmanager.sbins.encoder import DefaultEncodingProfile

class H264Encoder(VideoEncoder):
    def __init__(self, bytestream="False", profile=DefaultEncodingProfile()):
        self.description = "h264 encoder"
        self.type = "video"
        if hasattr(profile, 'keyframe_freq'):
            keyframe_freq = profile.keyframe_freq
        else:
            keyframe_freq = 0
        sbin = "x264enc bitrate=%s threads=%s byte-stream=%s key-int-max=%s" %(profile.video_bitrate, profile.encoding_threads, bytestream, keyframe_freq)
        VideoEncoder.__init__(self, sbin, profile)

from gstmanager.sbins.encoder import AudioEncoder

class AACEncoder(AudioEncoder):
    def __init__(self, profile=DefaultEncodingProfile()):
        self.description = "AAC encoder"
        self.type = "audio"
        sbin = "faac bitrate=%s profile=2" %profile.audio_bitrate
        AudioEncoder.__init__(self, sbin)
