#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
gstmanager: convenience fonctions for gstreamer pipeline manipulation 
@author Florent Thiery
"""

import logging
import gobject
logger = logging.getLogger('gstmanager')

import gst
pipeline_desc = "videotestsrc ! xvimagesink"
from event import EventLauncher

class PipelineManager(EventLauncher):
    def __init__(self, pipeline_string=None):
        EventLauncher.__init__(self)
        if pipeline_string is not None: 
            self.parse_description(pipeline_string)
        else:
            self.pipeline = gst.Pipeline()
            self.activate_bus()

    def avlink(self, bin1, bin2):
        self.vlink(bin1, bin2)
        self.alink(bin1, bin2)

    def vlink(self, bin1, bin2):
        voutput = bin1.get_pad("voutput")
        vinput = bin2.get_pad("vinput")
        voutput.link(vinput)

    def alink(self, bin1, bin2):
        aoutput = bin1.get_pad("aoutput")
        ainput = bin2.get_pad("ainput")
        aoutput.link(ainput)

    def redefine_pipeline(self, widget=None, new_string="Default"):
        #self.stop()
        self.parse_description(new_string)

    def parse_description(self, string):
        logger.info("parsing pipeline description: %s" %string)
        self.pipeline_string = string
        self.pipeline = gst.parse_launch(string)
        self.activate_bus()

    def activate_bus(self):
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_message)

    def run(self, *args):
        logger.info("Starting pipeline")
        self.pipeline.set_state(gst.STATE_PLAYING)

    def pause(self, *args):
        logger.info("Pausing pipeline")
        self.pipeline.set_state(gst.STATE_PAUSED)

    def stop(self, *args):
        logger.info( "Stopping pipeline")
        self.pipeline.set_state(gst.STATE_NULL)

    def get_state(self, *args):
        state = self.pipeline.get_state()[1]
        return state.value_name

    def get_position(self, *args):
        position = self.pipeline.query_position(gst.FORMAT_TIME)[0]
        return self.convert_time_to_seconds(position)

    def get_duration(self, *args):
        duration = self.pipeline.query_duration(gst.FORMAT_TIME)[0]
        return self.convert_time_to_seconds(duration)

    def has_duration(self):
        duration = self.pipeline.query_duration(gst.FORMAT_TIME)[0]
        logger.info(duration)
        if duration != -1:
            return True
        else:
            return False

    def seek_seconds(self, widget, getter):
        logger.info( "Trying to seek to %s" %getter())
        self.pipeline.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, getter()*1000000000)

    def send_eos(self, *args):
        logger.info("Sending EOS")
        event = gst.event_new_eos()
        gst.Element.send_event(self.pipeline, event)

    def set_caps(self, caps_name="capsfilter", caps=None):
        logger.info("Setting caps %s on capsfilter named " %(caps, caps_name))
        capsfilter = self.pipeline.get_by_name(caps_name)
        GstCaps = gst.caps_from_string(caps)
        capsfilter.set_property("caps",GstCaps)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            logger.info("Error: %s %s" %(err, debug))
        elif t == gst.MESSAGE_EOS:
            self.launchEvent("eos")
        elif t == gst.MESSAGE_ELEMENT:
            name = message.structure.get_name()
            res = message.structure
            self.launchEvent(name, res)
        else:
            logger.debug( "got unhandled message type %s, structure %s" %(t, message))

    def convert_time_to_seconds(self, time):
        if time == -1:
            time = "infinite"
        else:
            time = time / 1000000000
        return time

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
