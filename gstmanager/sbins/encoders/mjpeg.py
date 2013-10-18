#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.encoder import VideoEncoder, AudioEncoder
from gstmanager.sbins.muxer import Muxer

class JpegEncoder(VideoEncoder):
    def __init__(self, profile):
        self.description = "Jpeg encoder"
        self.type = "video"
        #sbin = "jpegenc"
        sbin = "queue name=ffenc_mjpeg ! ffenc_mjpeg bitrate=40000000"
        VideoEncoder.__init__(self, sbin, profile=profile)

class VorbisEncoder(AudioEncoder):
    def __init__(self, profile):
        self.description = "Vorbis encoder"
        self.type = "audio"
        sbin = "vorbisenc bitrate=%s" %profile.audio_bitrate
        AudioEncoder.__init__(self, sbin)

class IdentityEncoder(AudioEncoder):
    def __init__(self, profile):
        self.description = "Identity encoder"
        self.type = "audio"
        sbin = "identity silent=true" 
        AudioEncoder.__init__(self, sbin)

class MkvMuxer(Muxer):
    def __init__(self):
        self.description = "Mkv Muxer"
        self.type = "audio/video"
        sbin = "matroskamux min-index-interval=1000000000"
        Muxer.__init__(self, sbin)

from gstmanager.sbins.encoder import FileEncoder
from gstmanager.profiles.ogg import OggDefaultRecordingProfile

class MjpegEncoder(FileEncoder):
    def __init__(self, filename="/tmp/test.mkv",profile=OggDefaultRecordingProfile()):
        FileEncoder.__init__(self, filename)
        self.venc = JpegEncoder(profile)
        self.aenc = IdentityEncoder(profile)
        #self.aenc = VorbisEncoder(profile)
        self.muxer = MkvMuxer()
        self.add_many(self.venc, self.aenc, self.muxer)
        self.tags = ["a_src", "v_src"]
        self.type = "audio-video"
        self.description = "Mkv/mjpeg to File Encoder"
        self.sbin = "%s muxer_tee. ! filesink location=%s" %(self.pipeline_desc, filename)
