import gst
from gstmanager.binmanager import BinManager

class PreviewTee(BinManager):
    # This Bin is intended to serve as plug-and-preview element

    def __init__(self):
        BinManager.__init__(self, name="PreviewTee")

        # Video elements
        vq0 = self.add_element("queue")
        vtee = self.add_element("tee")
        vq1 = self.add_element("queue")
        vq2 = self.add_element("queue")
        vcol = self.add_element("ffmpegcolorspace")
        vsink = self.add_element("xvimagesink")
        #vsink = gst.element_factory_make("glimagesink")
        #vsink.set_property("sync", False)

        vq0.link(vtee)
        vtee.link(vq1)
        vq1.link(vcol)
        vcol.link(vsink)
        vtee.link(vq2)

        voutput_pad = vq2.get_pad("src")
        self.add_ghostpad_from_static("voutput", voutput_pad)

        vinput_pad = vq0.get_pad("sink")
        self.add_ghostpad_from_static("vinput", vinput_pad)
        
        # Audio elements
        aq0 = self.add_element("queue")
        atee = self.add_element("tee")
        aq1 = self.add_element("queue")
        level = self.add_element("level")
        # add other analysis elements here
        asink = self.add_element("alsasink")
        aq2 = self.add_element("queue")

        aq0.link(atee)
        atee.link(aq1)
        aq1.link(level)
        level.link(asink)
        atee.link(aq2)

        aoutput_pad = aq2.get_pad("src")
        self.add_ghostpad_from_static("aoutput", aoutput_pad)

        ainput_pad = aq0.get_pad("sink")
        self.add_ghostpad_from_static("ainput", ainput_pad)
