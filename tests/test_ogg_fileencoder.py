#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SBins are for "String Bins": manipulating Bins directly with Python can be tricky, notably because of the API differences (and lack of documentation porting) with the C API. Using string-based bin-like manipulation offers some flexibility over raw bin programming

from gstmanager.event import EventListener

import logging
logger = logging.getLogger("ogg-encoder")

from gstmanager.profile import DefaultEncodingProfile

class OggRecordingProfile(DefaultEncodingProfile):
    def __init__(self):
        DefaultEncodingProfile.__init__(self)
        self.video_width = 640
        self.video_height = 480

class Actioner(EventListener):
    def __init__(self):
        EventListener.__init__(self)
        self.registerEvent("eos")
        self.registerEvent("caps")
        self.registerEvent("encoding_progress")
        self.registerEvent("encoding_error")

    def evt_eos(self, event):
        logger.info("EOS Received")
        import sys
        sys.exit(0)

    def evt_encoding_progress(self, event):
        print "Filesize is %s" %event.content

    def evt_encoding_error(self, event):
        print "Error, encoding stalled"
        import sys
        sys.exit(1)

import logging, sys

logging.basicConfig(
    level=getattr(logging, "DEBUG"),
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    stream=sys.stderr
)

from gstmanager.sbinmanager import SBinManager
from gstmanager.gstmanager import PipelineManager

class OggEncodingTestApp(SBinManager, PipelineManager):
    def __init__(self, vsource, asource, previewsink):
        SBinManager.__init__(self)
        from gstmanager.sbins.encoders.ogg import OggEncoder
        profile = OggRecordingProfile()
        self.encoder = encoder = OggEncoder(filename="/tmp/test.ogg", profile=profile)
        self.add_many(vsource, asource, previewsink, encoder)
        PipelineManager.__init__(self, self.pipeline_desc)

if __name__ == '__main__':

    from gstmanager.sbins.sources.videotest import VideoTestSource
    v = VideoTestSource()

    from gstmanager.sbins.sources.alsa import AlsaSource
    a = AlsaSource(2)

    from gstmanager.sbins.sinks.xvimagesink import XVImageSink
    sink = XVImageSink()

    encoder = OggEncodingTestApp(v, a, sink)

    import gobject

    listener = Actioner()

    import gtk

    import gobject
    #gobject.timeout_add(10000, encoder.send_eos)

    gobject.timeout_add(100, encoder.run)
    gtk.main()
