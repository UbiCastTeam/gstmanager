#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':

    #import os
    #os.environ['GST_DEBUG'] = '3'

    import logging, sys

    logging.basicConfig(
        level=getattr(logging, "DEBUG"),
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        stream=sys.stderr
    )

    #from gstmanager.profile import DefaultRtpStreamingProfile
    #profile = DefaultRtpStreamingProfile()
    #profile.to_string()
    #from gstmanager.bins.rtpencoding import RtpEncodingBin
    #sink = RtpEncodingBin(profile)

    from gstmanager.profile import DefaultOggStreamingProfile
    profile = DefaultOggStreamingProfile()
    from gstmanager.bins.shoutcast import ShoutBin
    sink = ShoutBin(profile)

    from gstmanager.bins.testsrc import TestSrcBin
    src = TestSrcBin()

    from gstmanager.bins.previewtee import PreviewTee
    preview = PreviewTee()

    from gstmanager.gstmanager import PipelineManager
    pp = PipelineManager()
    p = pp.pipeline

    p.add(src, preview, sink)
    pp.vlink(src, preview)
    pp.vlink(preview, sink)
    pp.alink(src, preview)
    pp.alink(preview, sink)

    pp.run()

    import gtk
    gtk.gdk.threads_init()
    #import gobject
    #gobject.timeout_add(1000, test.get_sdp_info)
    gtk.main()
