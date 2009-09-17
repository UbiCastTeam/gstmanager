from gstmanager.event import EventListener 
import logging
logger = logging.getLogger('message_test')

class Actioner(EventListener):
    def __init__(self):
        EventListener.__init__(self)
        self.registerEvent("eos")
        self.registerEvent("GstVideoAnalyse")

    def evt_eos(self, event):
        logger.info("EOS Received")

    def evt_GstVideoAnalyse(self, event):
        source = event.content["source"]
        brightness = event.content["data"]["brightness"]
        variance = event.content["data"]["brightness-variance"]
        logger.info("New message from %s Brightness: %s Variance: %s" %(source, brightness, variance))

if __name__ == '__main__':
    import logging, sys

    logging.basicConfig(
        level=getattr(logging, "DEBUG"),
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        stream=sys.stderr
    )

    from gstmanager.gstmanager import PipelineManager
    pipeline_desc = "videotestsrc num-buffers=100 ! videobalance ! videoanalyse ! xvimagesink"

    actioner = Actioner()
    pipelinel = PipelineManager(pipeline_desc)
    pipelinel.run()


    import gtk
    gtk.main()

