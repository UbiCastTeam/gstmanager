#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
#os.environ['GST_DEBUG'] = '3'
#os.environ['GST_DEBUG'] = '2'

import logging
import gst
from gstmanager.binmanager import BinManager
logger = logging.getLogger('rtpencodingbin')
import gobject

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
        #vpad = vpay.get_pad("src")
        #vpad.connect('notify::caps', self.notify_caps)

        self.vsink = vsink = self.add_element("udpsink")
        vsink.set_property("host", profile.ip)
        vsink.set_property("port", profile.vport)
        self.set_caps(vcaps, "video/x-raw-yuv, format=(fourcc)I420, framerate=(fraction)%s/1, width=(int)%s, height=(int)%s, pixel-aspect-ratio=(fraction)1/1" %(profile.framerate, profile.width, profile.height))

        vqueue.link(vproc)
        vproc.link(vcaps)
        vcaps.link(venc)
        venc.link(vpay)
        vpay.link(vsink)

        vinput_pad = vqueue.get_pad("sink")
        self.add_ghostpad_from_static("vinput", vinput_pad)

        self.aqueue = aqueue = self.add_element("queue")
        self.aconv = aconv = self.add_element("audioconvert")
        self.aenc = aenc = self.add_element("faac")
        aenc.set_property("bitrate", profile.abitrate)
        self.apay = apay = self.add_element("rtpmp4gpay")
        self.asink = asink = self.add_element("udpsink")
        self.asink.set_property("host", profile.ip)
        asink.set_property("port", profile.aport)

        aqueue.link(aconv)
        aconv.link(aenc)
        aenc.link(apay)
        apay.link(asink)

        ainput_pad = aqueue.get_pad("sink")
        self.add_ghostpad_from_static("ainput", ainput_pad)

    def notify_caps(self, pad, caps):
        caps =  pad.get_caps()
        print caps

    def get_sdp_info(self):
        sdp_template = \
"v=0\n\
o=- 571622436 4192730712 IN IP4 127.0.0.1\n\
s=Gstreamer test\n\
i=Gstreamer-fastvdo test\n\
u=http://www.ubicast.eu\n\
e=support@fastvdo.com\n\
c=IN IP4 %s/64\n\
m=video %s RTP/AVP 96\n\
a=rtpmap:96 H264/90000\n\
a=control:trackID=1\n\
a=fmtp:96 profile-level-id=42e01e; packetization-mode=1; sprop-parameter-sets=Z0LgHtoC0EmwEAg=,aM4zyA==\n\
m=audio %s RTP/AVP 96\n\
a=rtpmap:96 mpeg4-generic/48000/2\n\
a=control:trackID=2\n\
a=fmtp:96 streamtype=5; profile-level-id=1; mode=AAC-hbr; config=0990; objectType=64; sizeLength=13; indexLength=3; indexDeltaLength=3" %(self.profile.ip, self.profile.vport, self.profile.aport)
        print sdp_template

if __name__ == '__main__':

    import logging, sys

    logging.basicConfig(
        level=getattr(logging, "DEBUG"),
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        stream=sys.stderr
    )

    from gstmanager.profile import DefaultStreamingProfile
    profile = DefaultStreamingProfile()
    profile.to_string()

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

    p.set_state(gst.STATE_PLAYING)

    import gtk
    gtk.gdk.threads_init()
    #import gobject
    #gobject.timeout_add(1000, test.get_sdp_info)
    gtk.main()
