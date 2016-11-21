#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.encoder import VideoEncoder
from gstmanager.sbins.encoder import DefaultEncodingProfile
from gstmanager.sbins.encoder import AudioEncoder


class H264Encoder(VideoEncoder):
    def __init__(self, bytestream="False", profiles=DefaultEncodingProfile()):
        self.description = "h264 encoder"
        self.type = "video"
        if isinstance(profiles, list):
            main_profile = profiles[0]
        else:
            main_profile = profiles
        if hasattr(main_profile, 'keyframe_freq'):
            keyframe_freq = main_profile.keyframe_freq
        else:
            keyframe_freq = 0
        sbin = "videobalance name=vlivemute ! x264enc bitrate=%s threads=%s byte-stream=%s key-int-max=%s" % (main_profile.video_bitrate, main_profile.encoding_threads, bytestream, keyframe_freq)
        VideoEncoder.__init__(self, sbin, main_profile)


class AACEncoder(AudioEncoder):
    def __init__(self, profiles=DefaultEncodingProfile(), index=0):
        self.description = "AAC encoder"
        self.type = "audio"
        if isinstance(profiles, list):
            main_profile = profiles[0]
        else:
            main_profile = profiles
        sbin = "volume name=alivemute%s ! faac bitrate=%s profile=2" % (index, main_profile.audio_bitrate)
        AudioEncoder.__init__(self, sbin)
