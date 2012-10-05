#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gst
audio_queue = 'queue max-size-bytes=0 max-size-buffers=0 max-size-time=%s' %(30*gst.SECOND)

class Muxer(object):
    index = 0
    def __init__(self, sbin_content):
        self.tags = ["a_enc_%s" %Muxer.index, "v_enc_%s" %Muxer.index]
        self.sbin = "%s_tee. ! %s name=a_mux_%s ! %s name=muxer ! queue ! tee name=muxer_tee %s_tee. ! queue name=v_mux_%s ! muxer." %(self.tags[0], audio_queue, Muxer.index, sbin_content, self.tags[1], Muxer.index)
        Muxer.index += 1
