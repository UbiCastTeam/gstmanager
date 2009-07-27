#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AVSource(object):
    def __init__(self, sbin_content):
        self.tags = ["av_src"]
        self.sbin = "%s ! queue ! tee name=%s_tee" %(sbin_content, self.tags[0])

class AudioSource(object):
    def __init__(self, sbin_content):
        self.tags = ["a_src"]
        self.sbin = "%s ! queue ! tee name=%s_tee" %(sbin_content, self.tags[0])

class VideoSource(object):
    def __init__(self, sbin_content):
        self.tags = ["v_src"]
        self.sbin = "%s ! queue ! tee name=%s_tee" %(sbin_content, self.tags[0])
