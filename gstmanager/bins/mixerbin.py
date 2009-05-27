#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gst
from binmanager import BinManager

class MixerBinManager(Bin):
    def __init__(self):
        BinManager.__init__(self)
        self.n_in = 0

        self.mixer = mixer = gst.element_factory_make("videomixer")
        self.add(mixer)

        output_pad = mixer.get_pad("src")
        self.add_ghostpad_from_static("output", output_pad)

        self.add_input_branch()

    def _add_input_pad(self, element):
        input_pad = element.get_pad("sink")
        name = "input%s" %self.n_in
        self.add_ghostpad_from_static(name, input_pad)
        self.n_in += 1

    def add_input_branch(self):
        alpha = gst.element_factory_make("alpha", "alpha%s" %self.n_in)
        alpha.set_property("alpha", 0.5)
        queue = gst.element_factory_make("queue")
        self.add(alpha, queue)
        queue.link(alpha)
        alpha.link(self.mixer)
        self._add_input_pad(queue)

    def set_input(self, number):
        for i in range(self.n_in):
            alpha = self.get_by_name("alpha%s" %i)
            if i == number:
                alpha.set_property("alpha", 1)
            else:
                alpha.set_property("alpha", 0)

    def get_nb_inputs(self):
        return self.n_in

