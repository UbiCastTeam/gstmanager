from gstmanager.event import EventListener 

def set_input(pipelinel, value):
    print "Switching to pad %s" %value
    selector = pipelinel.pipeline.get_by_name("select")
    pad = selector.get_pad("sink%s" %value)
    selector.set_property("active-pad", pad)
    #selector.emit("block")
    #selector.emit("switch", pad, -1, -1)

if __name__ == '__main__':

    from gstmanager.gstmanager import PipelineManager
    pipeline_desc = "videotestsrc is-live=true ! cairotimeoverlay ! queue ! input-selector name=select ! tee name=tee ! queue ! theoraenc ! oggmux name=mux ! filesink location=/tmp/test.ogg tee. ! queue ! xvimagesink videotestsrc pattern=2 is-live=true ! cairotimeoverlay ! queue ! select. audiotestsrc is-live=true ! vorbisenc ! queue ! mux."

    pipelinel = PipelineManager(pipeline_desc)
    pipelinel.run()

    selector = pipelinel.pipeline.get_by_name("select")
    print "Active pad: %s" %selector.get_property("active-pad")

    # Let's schedule some property changing
    import gobject
    gobject.timeout_add(2000, set_input, pipelinel, 1) 
    gobject.timeout_add(4000, set_input, pipelinel, 0) 
    gobject.timeout_add(7000, set_input, pipelinel, 1) 
    gobject.timeout_add(10000, pipelinel.send_eos) 

    import gtk
    gtk.main()
