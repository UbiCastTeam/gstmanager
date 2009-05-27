import gst
from binmanager import BinManager

class PreviewTee(BinManager):
    # This Bin is intended to serve as plug-and-preview element

    def __init__(self):
        BinManager.__init__(self)
        q0 = gst.element_factory_make("queue", "q0")
        tee = gst.element_factory_make("tee", "decoded_tee")
        q1 = gst.element_factory_make("queue", "q1")
        q2 = gst.element_factory_make("queue", "q2")
        ff = gst.element_factory_make("ffmpegcolorspace")
        #vsink = gst.element_factory_make("xvimagesink")
        vsink = gst.element_factory_make("glimagesink")

        self.add(q0, tee, q1, q2, ff, vsink)

        q0.link(tee)
        tee.link(q1)
        q1.link(ff)
        ff.link(vsink)
        tee.link(q2)

        output_pad = q2.get_pad("src")
        self.add_ghostpad_from_static("output", output_pad)

        input_pad = q0.get_pad("sink")
        self.add_ghostpad_from_static("input", input_pad)

