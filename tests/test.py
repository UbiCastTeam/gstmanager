from gstmanager.event import EventListener 

class EOS_actioner(EventListener):
    def __init__(self):
        EventListener.__init__(self)
        self.registerEvent("eos")

    def evt_eos(self):
        logger.info("EOS Recieved")

if __name__ == '__main__':
    import logging, sys

    logging.basicConfig(
        level=getattr(logging, "DEBUG"),
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        stream=sys.stderr
    )

    from gstmanager.gstmanager import PipelineManager
    pipeline_desc = "videotestsrc num-buffers=100 ! videobalance ! xvimagesink"

    pipelinel = PipelineManager(pipeline_desc)
    pipelinel.run()


    import gtk
    gtk.main()

