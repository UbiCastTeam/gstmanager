from gstmanager.event import EventListener 

class EOS_actioner(EventListener):
    # This class will subscribe to proxied eos messages
    def __init__(self):
        EventListener.__init__(self)
        self.registerEvent("eos")

    def evt_eos(self, event):
    # This is the callback used for every evt_MSGNAME received
        logger.info("EOS Recieved")

def set_brightness(pipelinel, value):
    # set_property_on_element example
    pipelinel.set_property_on_element(element_name="balance", property_name="brightness", value=value)

if __name__ == '__main__':
    import logging, sys

    logging.basicConfig(
        level=getattr(logging, "DEBUG"),
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        stream=sys.stderr
    )

    from gstmanager.gstmanager import PipelineManager
    pipeline_desc = "videotestsrc num-buffers=100 ! videobalance name=balance ! xvimagesink"

    pipelinel = PipelineManager(pipeline_desc)
    pipelinel.run()

    # Let's schedule some property changing
    import gobject
    gobject.timeout_add(2000, set_brightness, pipelinel, 0.2) 

    main_loop = gobject.MainLoop()
    main_loop.run()

