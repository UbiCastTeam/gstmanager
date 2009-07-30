#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.profile import DefaultEncodingProfile

class AudioEncoder(object):
    index = 0
    def __init__(self, sbin_content):
        self.tags = ["a_src_tee"]
        self.enc_tag = "a_enc_%s_tee" %AudioEncoder.index
        sbin_begin = "%s. ! queue ! audioconvert !" %self.tags[0]
        sbin_end = "! queue ! tee name=%s" %(self.enc_tag)
        self.sbin = "%s %s name=aencoder_%s %s" %(sbin_begin, sbin_content, AudioEncoder.index, sbin_end)
        AudioEncoder.index += 1

class VideoEncoder(object):
    index = 0
    def __init__(self, sbin_content, profile=DefaultEncodingProfile()):
        self.profile = profile
        self.tags = ["v_src_tee"]
        self.enc_tag = "v_enc_%s_tee" %VideoEncoder.index
        self.caps = "video/x-raw-yuv, format=(fourcc)I420, width=(int)%s, height=(int)%s, framerate=(fraction)25/1" %(profile.video_width, profile.video_height)
        sbin_begin = "%s. ! queue ! ffmpegcolorspace ! videorate ! videoscale ! %s !" %(self.tags[0], self.caps)
        sbin_end = "! queue ! tee name=%s" %self.enc_tag
        self.sbin = "%s %s name=vencoder_%s %s" %(sbin_begin, sbin_content, VideoEncoder.index, sbin_end)
        VideoEncoder.index += 1
