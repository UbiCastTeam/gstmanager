#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AudioEncoder(object):
    def __init__(self, sbin_content):
        self.tags = ["a_src"]
        self.enc_tag = "a_enc"
        sbin_begin = "%s_tee. ! queue ! audioconvert !" %self.tags[0]
        sbin_end = "! queue ! tee name=%s_tee" %(self.enc_tag)
        self.sbin = "%s %s name=aencoder %s" %(sbin_begin, sbin_content, sbin_end)

class VideoEncoder(object):
    def __init__(self, sbin_content):
        self.tags = ["v_src"]
        self.enc_tag = "v_enc"
        sbin_begin = "%s_tee. ! queue ! ffmpegcolorspace !" %self.tags[0]
        sbin_end = "! queue ! tee name=%s_tee" %self.enc_tag
        self.sbin = "%s %s name=vencoder %s" %(sbin_begin, sbin_content, sbin_end)
