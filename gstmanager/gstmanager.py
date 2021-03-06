#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
gstmanager: convenience fonctions for gstreamer pipeline manipulation 
@author Florent Thiery
"""

import logging, os

import gobject
logger = logging.getLogger('gstmanager')

import gst
import time
pipeline_desc = "videotestsrc ! xvimagesink"
import easyevent

class PipelineManager(easyevent.User):
    def __init__(self, pipeline_string=None, name=None, eos_cb=None, error_cb=None):
        easyevent.User.__init__(self)
        self.name = name
        self.start_time = None
        self.bus_msg_id = None
        self.error_cb = error_cb
        self.eos_cb = eos_cb
        if pipeline_string is not None: 
            self.parse_description(pipeline_string)
        else:
            if name is not None:
                self.pipeline = gst.Pipeline(name)
            else:
                self.pipeline = gst.Pipeline()
            self.activate_bus()

    def get_name(self):
        if hasattr(self, "pipeline"):
            return self.pipeline.get_name()

    def redefine_pipeline(self, widget=None, new_string=None):
        if new_string is None:
            new_string = self.pipeline_desc
            logger.debug("Reinitializing pipeline")
        else:
            logger.debug('Redefining pipeline %s pipeline to %s' %(self.pipeline.get_name(), new_string))
        self.clean_pipeline()
        self.parse_description(new_string)

    def is_running(self):
        if hasattr(self, "pipeline"):
            if self.get_state() == "GST_STATE_PLAYING":
                logger.debug("Pipeline is up and running")
                return True
            else:
                logger.debug("Pipeline is not in running state")
                return False
        else:
                logger.debug("Pipeline has not been initialized yet")
                return False

    def parse_description(self, string):
        self.pipeline_desc = string
        hstring = self.get_pastable_string()
        if self.name is None:
            name = "(unnamed)"
        else:
            name=  self.name
        logger.debug("Launching pipeline %s; copy-paste the following for manual debugging: \n\ngst-launch-0.10 %s\n" %(name, hstring))
        try:
            self.pipeline = gst.parse_launch(string)
        except Exception, e:
            if self.name is not None:
                e = "%s : %s" %(self.name, e)
            logger.error('Error in parse_description: %s\ngst-launch-0.10 %s' %(e, hstring))
            if self.error_cb:
                self.error_cb('Error in parse_description: %s' %e)
            self.launch_event('gst_error', str(e))
            return
        if self.name is not None:
            self.pipeline.set_name(self.name)
        self.activate_bus()

    def activate_bus(self):
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        if self.bus_msg_id is not None:
            logger.warning('Bus is already watched !')
        self.bus_msg_id = self.bus.connect('message', self.on_message)

    def disable_bus(self):
        self.bus.remove_signal_watch()
        if self.bus_msg_id is not None:
            self.bus.disconnect(self.bus_msg_id)
            self.bus_msg_id = None
        else:
            logger.warning('Bus has already been disconnected')

    def clean_pipeline(self):
        logger.debug('Cleaning pipeline')
        self.disable_bus()
        del self.pipeline
        # TODO count refs and liberate them

    def run(self, *args):
        self.start_time = time.time()
        logger.info("Starting pipeline %s" %self.pipeline.get_name())
        self.launch_event("sos", self.pipeline)
        self.pipeline.set_state(gst.STATE_PLAYING)
        # Returning false if it was called by a gobject.timeout 
        return False

    def play(self, *args):
        self.run()

    def pause(self, *args):
        logger.info("Pausing pipeline")
        self.pipeline.set_state(gst.STATE_PAUSED)

    def stop(self, *args):
        if hasattr(self, 'pipeline'):
            name = self.pipeline.get_name()
            logger.info('Stopping pipeline %s' %name)
            before_teardown = time.time()
            self.pipeline.set_state(gst.STATE_NULL)
            if self.start_time is not None:
                stop_time = time.time()
                total_dur = int(stop_time - self.start_time)
                teardown_time_ms = int(round((stop_time - before_teardown)*1000))
                logger.debug("Execution of pipeline %s ended after %ss of execution, teardown took %sms" %(name, total_dur, teardown_time_ms))
                self.start_time = None
        else:
            logger.error('Cannot stop non-running pipeline')

    def get_runtime(self):
        if self.start_time:
            now = time.time()
            runtime = now - self.start_time
            return runtime

    def get_string_tag(self, taglist):
        return gst.Structure.to_string(taglist)

    def get_state(self, *args):
        state = self.pipeline.get_state()[1]
        return state.value_name

    def get_position(self, *args):
        try:
            position = self.pipeline.query_position(gst.FORMAT_TIME)[0]
            return self.convert_time_to_seconds(position)
        except gst.QueryError:
            logger.error('Position query failed')
            return 0

    def get_duration(self, *args):
        try:
            duration = self.pipeline.query_duration(gst.FORMAT_TIME)[0]
            return self.convert_time_to_seconds(duration)
        except gst.QueryError:
            logger.error('Duration query failed')
            return 0

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
        logger.info("Sending EOS on %s" %self.pipeline.get_name())
        event = gst.event_new_eos()
        gst.Element.send_event(self.pipeline, event)

    def set_caps(self, caps_name="capsfilter", caps=None):
        logger.info("Setting caps %s on capsfilter named %s" %(caps, caps_name))
        capsfilter = self.pipeline.get_by_name(caps_name)
        GstCaps = gst.caps_from_string(caps)
        capsfilter.set_property("caps",GstCaps)

    def set_property_on_element(self, element_name="whatever", property_name="property", value="value"):
        logger.debug("Setting value %s to property %s of element %s" %(value, property_name, element_name))
        elt = self.pipeline.get_by_name(element_name)
        if elt is not None:
            elt.set_property(property_name, value)
        else:
            logger.error('Element %s not found' %element_name)

    def get_property_on_element(self, element_name="whatever", property_name="property"):
        elt = self.pipeline.get_by_name(element_name)
        if elt is not None:
            result = elt.get_property(property_name)
            logger.debug("Getting value of property %s of element %s: %s" %(property_name, element_name, result))
            return result
        else:
            logger.error('Element %s not found' %element_name)

    def activate_caps_reporting_on_element(self, element_name="whatever"):
        logger.debug("Activating caps reporting on element %s" %element_name)
        elt = self.pipeline.get_by_name(element_name)
        out_pad = elt.get_pad("src")
        out_pad.set_setcaps_function(self.send_caps)

    def activate_polling_of_property_on_element(self, element_name="whatever", property="property", interval_ms=1000):
        gobject.timeout_add(interval_ms, self.poll_property, element_name, property)
        self.do_poll = True

    def deactivate_pollings(self):
        self.do_poll = False

    def poll_property(self, element_name, property):
        value = self.get_property_on_element(element_name, property)
        self.launch_event("%s_value_change" %property, {"source": element_name, "property": property, "value": value})
        return self.do_poll

    def send_caps(self, pad, caps):
        logger.debug("Got negociated caps")
        caps_str = caps.to_string()
        self.launch_event("caps", caps_str)
        return True

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            error_string = "%s %s" %(err, debug)
            if self.error_cb:
                self.error_cb(error_string)
            logger.info("Error: %s on pipeline:\n%s" %(error_string, self.get_pastable_string()))
            self.launch_event("gst_error", error_string)
        elif t == gst.MESSAGE_EOS:
            self.launch_event("eos", self.pipeline.get_name())
            if self.eos_cb:
                self.eos_cb("eos")
        elif t == gst.MESSAGE_ELEMENT:
            name = message.structure.get_name()
            res = message.structure
            source = (str(message.src)).split(":")[2].split(" ")[0]
            self.launch_event(name, {"source": source, "data": res})
            self.launch_event('gst_element_message', {"source": source, "name": name, "data": res})
        elif t == gst.MESSAGE_TAG:
            name = message.structure.get_name()
            res = message.structure
            source = (str(message.src)).split(":")[2].split(" ")[0]
            self.launch_event(name, {"source": source, "data": res})
            self.launch_event('gst_element_tag', {"source": source, "name": name, "data": res})            
        else:
            #logger.debug( "got unhandled message type %s, structure %s" %(t, message))
            pass

    def dump_dot_file(self, basename='pipeline'):
        directory = os.environ.get('GST_DEBUG_DUMP_DOT_DIR', None)
        if directory:
            dotfile = os.path.join(directory, '%s.dot' %basename)
            if os.path.isfile(dotfile):
                logger.debug('Removing existing dotfile %s' %dotfile)
                os.remove(dotfile)
            logger.debug('Dumping graph to %s' %dotfile)
            gst.DEBUG_BIN_TO_DOT_FILE (self.pipeline, gst.DEBUG_GRAPH_SHOW_ALL, basename)
            return dotfile
        else:
            logger.error('You need to define the GST_DEBUG_DUMP_DOT_DIR env var to dump a .dot graph of the running pipeline')
            return None

    def convert_time_to_seconds(self, time):
        if time == -1:
            time = "infinite"
        else:
            time = time / 1000000000
        return time

    def get_pastable_string(self, string=None):
        if not string:
            hstring = string = self.pipeline_desc
        hstring = string
        parts = string.split(" ! ")
        for part in parts:
            if part.startswith("video/") or part.startswith("audio/") or part.startswith("image/"):
                hpart = '"%s"' %part
                hstring = hstring.replace('! %s !' %part, '! %s !' %hpart)
        return hstring

if __name__ == '__main__':

    import logging, sys

    logging.basicConfig(
        level=getattr(logging, "DEBUG"),
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        stream=sys.stderr
    )

    pipeline_desc = "videotestsrc is-live=true ! fakesink"
    pipelinel = PipelineManager(pipeline_desc)
    pipelinel.run()
    main_loop = gobject.MainLoop()
    main_loop.run()
