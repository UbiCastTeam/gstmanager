from gstmanager.event import EventListener 

import logging
logger = logging.getLogger("test_caps_reporting")

class Actioner(EventListener):
    # This class will subscribe to proxied eos messages
    def __init__(self):
        EventListener.__init__(self)
        self.registerEvent("eos")
        self.registerEvent("caps")

    def evt_eos(self, event):
    # This is the callback used for every evt_MSGNAME received
        logger.info("EOS Recieved")

    def evt_caps(self, event):
        logger.info("Caps received, %s" %event.content)

if __name__ == '__main__':
    import logging, sys

    logging.basicConfig(
        level=getattr(logging, "DEBUG"),
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        stream=sys.stderr
    )

    a = Actioner()

    from gstmanager.gstmanager import PipelineManager
    pipeline_desc = "audiotestsrc ! faac ! rtpmp4gpay name=pay ! udpsink"

    pipelinel = PipelineManager(pipeline_desc)

    import gobject
    gobject.idle_add(pipelinel.activate_caps_reporting_on_element, "pay")
    gobject.idle_add(pipelinel.run)
    import gtk
    gtk.main()


