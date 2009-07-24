#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.sbins.sources.videotest import VideoTestSource
v = VideoTestSource()

from gstmanager.sbins.sinks.ximagesink import XImageSink
s = XImageSink()

pipeline_desc = "%s ! %s" %(v.sbin, s.sbin)
print pipeline_desc

if __name__ == '__main__':
    import logging, sys

    logging.basicConfig(
        level=getattr(logging, "DEBUG"),
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        stream=sys.stderr
    )

    from gstmanager.gstmanager import PipelineManager
    pipelinel = PipelineManager(pipeline_desc)
    pipelinel.run()
    import gtk
    gtk.main()
