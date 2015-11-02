#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gstmanager.event import EventListener

class Test(EventListener):
    def __init__(self):
        EventListener.__init__(self)
        self.registerEvent("drop_value_change")

    def evt_drop_value_change(self, event):
        data = event.content["value"]
        src = event.content["source"]
        property = event.content["property"]
        print "%s reports %s prop change to value %s" %(src, property, data)

from gstmanager.gstmanager import PipelineManager

caps_in = "video/x-raw-yuv, format=(fourcc)YUY2, width=(int)320, height=(int)240, framerate=(fraction)30/1"
caps_out = "video/x-raw-yuv, format=(fourcc)YUY2, width=(int)320, height=(int)240, framerate=(fraction)25/1"
pip = "videotestsrc ! %s ! videorate ! %s ! fakesink" %(caps_in, caps_out)

p = PipelineManager(pip)

p.play()
p.activate_polling_of_property_on_element(element_name="videorate0", property="drop", interval_ms=500)
print "Will poll element videorate for drop values for 10 seconds on 500ms interval"

t = Test()

import gobject
main_loop = gobject.MainLoop()
gobject.timeout_add_seconds(10, p.deactivate_pollings)

gobject.timeout_add_seconds(12, main_loop.quit)
main_loop.run()
