#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.profile import DefaultEncodingProfile

class AudioEncoder(object):
    def __init__(self, sbin_content):
        self.tags = ["a_src"]
        self.enc_tag = "a_enc"
        sbin_begin = "%s_tee. ! queue ! audioconvert !" %self.tags[0]
        sbin_end = "! queue ! tee name=%s_tee" %(self.enc_tag)
        self.sbin = "%s %s name=aencoder %s" %(sbin_begin, sbin_content, sbin_end)

class VideoEncoder(object):
    def __init__(self, sbin_content, profile=DefaultEncodingProfile()):
        self.profile = profile
        self.tags = ["v_src"]
        self.enc_tag = "v_enc"
        self.caps = "video/x-raw-yuv, format=(fourcc)I420, width=(int)%s, height=(int)%s, framerate=(fraction)25/1" %(profile.video_width, profile.video_height)
        sbin_begin = "%s_tee. ! queue ! ffmpegcolorspace ! videorate ! videoscale ! %s !" %(self.tags[0], self.caps)
        sbin_end = "! queue ! tee name=%s_tee" %self.enc_tag
        self.sbin = "%s %s name=vencoder %s" %(sbin_begin, sbin_content, sbin_end)
