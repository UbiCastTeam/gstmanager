import easyevent
import gobject
import time

class Actioner(easyevent.User):
    def __init__(self):
        easyevent.User.__init__(self)
        self.register_event("caps")

    def evt_caps(self, event):
        print "Caps received, %s" %event.content

if __name__ == '__main__':

    a = Actioner()

    from gstmanager.gstmanager import PipelineManager
    pipeline_desc = "audiotestsrc ! faac ! rtpmp4gpay name=pay ! udpsink host=127.0.0.1 port=1234 name=sink"

    pipelinel = PipelineManager(pipeline_desc)

    def get_time(time_epoch):
        if time_epoch == 0:
            time_epoch = "never"
        else:
            time_epoch = time.ctime(time_epoch/1000000000)
        return time_epoch

    def get_udp_stats():
        sink = pipelinel.pipeline.get_by_name("sink")
        bytes_sent, packets_sent, connect_time, disconnect_time = sink.emit("get-stats", "127.0.0.1", 1234)

        print "bytes sent: %s, packets sent: %s, connect_time: %s disconnect_time: %s" %(bytes_sent, packets_sent, get_time(connect_time), get_time(disconnect_time))
        return True

    gobject.timeout_add(1000, get_udp_stats)
    gobject.threads_init()
    gobject.idle_add(pipelinel.activate_caps_reporting_on_element, "pay")
    gobject.idle_add(pipelinel.run)
    main_loop = gobject.MainLoop()
    main_loop.run()
