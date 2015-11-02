#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SBins are for "String Bins": manipulating Bins directly with Python can be tricky, notably because of the API differences (and lack of documentation porting) with the C API. Using string-based bin-like manipulation offers some flexibility over raw bin programming

import logging, sys

logging.basicConfig(
    level=getattr(logging, "DEBUG"),
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    stream=sys.stderr
)

from gstmanager.sbins.sources.videotest import VideoTestSource
v = VideoTestSource()

from gstmanager.sbins.sinks.ximagesink import XImageSink
s = XImageSink()

from gstmanager.sbins.sources.audiotest import AudioTestSource
s2 = AudioTestSource()

from gstmanager.sbins.sinks.alsa import AlsaSink
s3 = AlsaSink()

from gstmanager.sbins.encoders.ogg import OggEncoder
e = OggEncoder("/tmp/test.ogg")

from gstmanager.sbinmanager import SBinManager
man = SBinManager()

'''
man.add(v)
man.add(s)
man.add(a)
man.add(s2)
man.add(a2)
man.add(s3)
man.add(e)
'''
man.add_many(v, s, s2, s3, e)

if __name__ == '__main__':

    from gstmanager.gstmanager import PipelineManager
    pipelinel = PipelineManager(man.pipeline_desc)
    pipelinel.run()
    import gobject
    gobject.timeout_add(2000, pipelinel.send_eos)
    gobject.timeout_add(3500, man.get_pipeline)
    main_loop = gobject.MainLoop()
    main_loop.run()
