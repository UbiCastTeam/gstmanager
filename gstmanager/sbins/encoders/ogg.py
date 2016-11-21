#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.encoder import VideoEncoder, AudioEncoder
from gstmanager.sbins.muxer import Muxer

class TheoraEncoder(VideoEncoder):
    def __init__(self, profile):
        self.description = "Theora encoder"
        self.type = "video"
        sbin = "theoraenc bitrate=%s keyframe-auto=False keyframe-force=%s keyframe-freq=%s" %(profile.video_bitrate, profile.keyframe_freq, profile.keyframe_freq)
        VideoEncoder.__init__(self, sbin, profile=profile)

    def set_index(self, index):
        VideoEncoder.set_index(index)

class VorbisEncoder(AudioEncoder):
    def __init__(self, profile):
        self.description = "Vorbis encoder"
        self.type = "audio"
        sbin = "vorbisenc bitrate=%s" %profile.audio_bitrate
        AudioEncoder.__init__(self, sbin)

    def set_index(self, index):
        AudioEncoder.set_index(index)

class OggMuxer(Muxer):
    def __init__(self):
        self.description = "Ogg Muxer"
        self.type = "audio/video"
        sbin = "oggmux"
        Muxer.__init__(self, sbin)

    def set_index(self, index):
        Muxer.set_index(index)

from gstmanager.sbins.encoder import FileEncoder
from gstmanager.profiles.ogg import OggDefaultRecordingProfile

class OggEncoder(FileEncoder):
    def __init__(self, filename="/tmp/test.ogg",profile=OggDefaultRecordingProfile()):
        FileEncoder.__init__(self, filename)

        self.venc = TheoraEncoder(profile)
        self.aenc = VorbisEncoder(profile)
        self.muxer = OggMuxer()
        self.add_many(self.venc, self.aenc, self.muxer)
        self.tags = ["a_src", "v_src"]
        self.type = "audio-video"
        self.description = "Ogg to File Encoder"
        self.sbin = "%s muxer_tee. ! filesink location=%s" %(self.pipeline_desc, filename)

class MkvTheoraEncoder(FileEncoder):
    def __init__(self, filename="/tmp/test.mkv",profile=OggDefaultRecordingProfile()):
        FileEncoder.__init__(self, filename)

        self.venc = TheoraEncoder(profile)
        self.aenc = VorbisEncoder(profile)
        from mjpeg import MkvMuxer
        self.muxer = MkvMuxer()
        self.add_many(self.venc, self.aenc, self.muxer)
        self.tags = ["a_src", "v_src"]
        self.type = "audio-video"
        self.description = "Mkv/Theora/Vorbis to File Encoder"
        self.sbin = "%s muxer_tee. ! filesink location=%s" %(self.pipeline_desc, filename)
