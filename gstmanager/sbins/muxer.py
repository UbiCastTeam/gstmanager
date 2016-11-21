#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gst
audio_queue = 'queue max-size-bytes=0 max-size-buffers=0 max-size-time=%s' %(30*gst.SECOND)
muxer_queue = 'queue max-size-bytes=0 max-size-buffers=0 max-size-time=%s' %(5*gst.SECOND)

class Muxer(object):
    index = 0
    def __init__(self, sbin_content):
        self.tags = ["a_enc_%s" %Muxer.index, "v_enc_%s" %Muxer.index]
        self.sbin = "%s_tee. ! %s name=a_mux_%s ! %s name=muxer ! tee name=muxer_tee %s_tee. ! %s name=v_mux_%s ! muxer." %(self.tags[0], audio_queue, Muxer.index, sbin_content, self.tags[1], muxer_queue, Muxer.index)
        Muxer.index += 1

    def set_index(self, index):
        Muxer.index = 0