#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import gst
from gstmanager.binmanager import BinManager
logger = logging.getLogger('rtpencodingbin')

class RtpEncodingBin(BinManager):
    def __init__(self, encoding_profile):
        BinManager.__init__(self, name="RtpEncodingBin")

        self.profile = profile = encoding_profile

        self.vqueue = vqueue = self.add_element("queue")
        self.vproc = vproc = self.add_element("videoscale")
        self.vcaps = vcaps = self.add_element("capsfilter")
        self.venc = venc = self.add_element("x264enc")
        self.venc.set_properties("bitrate", profile.vbitrate, "byte-stream", True, "threads", 4)

        self.vpay = vpay = self.add_element("rtph264pay")
        self.vsink = vsink = self.add_element("udpsink")
        self.vsink.set_properties("host", profile.ip, "port", profile.vport)
        self.set_caps(vcaps, "video/x-raw-yuv, format=(fourcc)I420, framerate=(fraction)%s/1, width=(int)%s, height=(int)%s, pixel-aspect-ratio=(fraction)1/1" %(profile.framerate, profile.width, profile.height))

        vqueue.link(vproc)
        vproc.link(vcaps)
        vcaps.link(venc)
        venc.link(vpay)
        vpay.link(vsink)

        vinput_pad = vqueue.get_pad("sink")
        self.add_ghostpad_from_static("vinput", vinput_pad)

        self.aqueue = aqueue = self.add_element("queue")
        self.aenc = aenc = self.add_element("faac")
        aenc.set_property("bitrate", profile.abitrate)
        self.apay = apay = self.add_element("rtpmp4gpay")
        self.vsink = vsink = self.add_element("udpsink")
        self.vsink.set_properties("host", profile.ip, "port", profile.aport)

        aqueue.link(aenc)
        aenc.link(apay)
        apay.link(vsink)

        ainput_pad = aqueue.get_pad("sink")
        self.add_ghostpad_from_static("ainput", ainput_pad)

    def get_sdp_info(self):
        #print self.get_state()
        #if self.get_state() == GST_STATE_PLAYING:
        if True:
            paypad = self.vsink.get_pad("sink")
            #caps = paypad.get_caps()
            caps = paypad.get_negotiated_caps()
            caps = caps.to_string()
            logger.debug("Negociated caps are %s" %caps)
            return False
        else:
            logger.debug("Need to run the Bin first to get negociated caps")
            return False

if __name__ == '__main__':
    def bla(arg):
        print "AFAFFAZF %s" %arg

    import logging, sys

    logging.basicConfig(
        level=getattr(logging, "DEBUG"),
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        stream=sys.stderr
    )

    from gstmanager.profile import DefaultStreamingProfile
    profile = DefaultStreamingProfile() 

    test = RtpEncodingBin(profile)

    #from gstmanager.gstmanager import PipelineManager
    #p = PipelineManager("videotestsrc ! queue name=src")
    p = gst.parse_launch("videotestsrc ! queue name=src")
    #src = p.pipeline.get_by_name("src")
    src = p.get_by_name("src")
    #p.pipeline.add(test)
    p.add(test)
    src.link(test)

    test.vpay.connect('notify::caps', bla)
    #test.run()
    #p.run()
    p.set_state(gst.STATE_PLAYING)
    #test.get_sdp_info()
    # TEST
    #vpad = test.vsink.get_pad("sink")

    import gtk
    gtk.main()
