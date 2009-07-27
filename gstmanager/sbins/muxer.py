#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Muxer(object):
    def __init__(self, sbin_content):
        self.tags = ["a_enc", "v_enc"]
        self.sbin = "a_enc_tee. ! queue ! %s name=muxer ! queue ! tee name=muxer_tee v_enc_tee. ! queue ! muxer." %sbin_content
