#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Muxer(object):
    index = 0
    def __init__(self, sbin_content):
        self.tags = ["a_enc_%s" %Muxer.index, "v_enc_%s" %Muxer.index]
        self.sbin = "%s_tee. ! queue ! %s name=muxer ! queue ! tee name=muxer_tee %s_tee. ! queue ! muxer." %(self.tags[0], sbin_content, self.tags[1])
        Muxer.index += 1
