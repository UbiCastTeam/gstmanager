#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gst
import logging
logger = logging.getLogger('binmanager')
from event import EventLauncher

class BinManager(gst.Bin, EventLauncher):
    def __init__(self, name=None):
        gst.Bin.__init__(self)
        EventLauncher.__init__(self)
        if name is not None:
            self.name = name
            self.set_property("name", name)

    def _create_ghostpad(self, name, pad):
        logger.debug("Creating ghostpad %s" %name)
        ghost_pad = gst.GhostPad(name, pad)
        return ghost_pad

    def add_ghostpad_from_static(self, name, pad):
        gpad = self._create_ghostpad(name, pad)
        self.add_pad(gpad)

    def add_element(self, name):
        logger.debug("Adding element %s" %name)
        elt = gst.element_factory_make(name)
        self.add(elt)
        return elt

    def set_caps(self, capsfilter, caps):
        logger.debug("Setting caps %s" %caps)
        gstcaps = gst.caps_from_string(caps)
        capsfilter.set_property("caps", gstcaps)

    def play(self):
        self.run()

    def start(self):
        self.run()

    def stop(self):
        logger.info("Stopping Bin %s" %self.name)
        self.set_state(gst.STATE_NULL)

    def run(self, *args):
        logger.info("Starting Bin %s" %self.name)
        self.set_state(gst.STATE_PLAYING)

    def pause(self, *args):
        logger.info("Pausing Bin %s" %self.name)

    def get_state(self):
        state = self.get_state()[1]
        logger.debug("Getting state of Bin %s, state is %s" %(self.name, state.value_name))
        return state.value_name

if __name__ == '__main__':

    import logging, sys

    logging.basicConfig(
        level=getattr(logging, "DEBUG"),
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        stream=sys.stderr
    )
    pipelinel = PipelineManager(pipeline_desc)
    pipelinel.run()
    import gtk
    gtk.main()
