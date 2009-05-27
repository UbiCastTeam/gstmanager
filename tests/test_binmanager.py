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

    from gstmanager.profile import DefaultStreamingProfile
    profile = DefaultStreamingProfile()
    profile.to_string()

    from gstmanager.bins.rtpencoding import RtpEncodingBin
    rtpsink = RtpEncodingBin(profile)

    from gstmanager.bins.testsrc import TestSrcBin
    src = TestSrcBin()

    from gstmanager.bins.previewtee import PreviewTee
    preview = PreviewTee()

    from gstmanager.gstmanager import PipelineManager
    pp = PipelineManager()
    p = pp.pipeline

    p.add(src, preview, rtpsink)
    voutput = src.get_pad("voutput")
    vinput = preview.get_pad("vinput")
    voutput.link(vinput)
    voutput2 = preview.get_pad("voutput")
    vinput2 = rtpsink.get_pad("vinput")
    voutput2.link(vinput2)
    aoutput = src.get_pad("aoutput")
    ainput = rtpsink.get_pad("ainput")
    aoutput.link(ainput)

    pp.run()

    import gtk
    gtk.gdk.threads_init()
    #import gobject
    #gobject.timeout_add(1000, test.get_sdp_info)
    gtk.main()
