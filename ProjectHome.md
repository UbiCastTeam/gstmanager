[GstManager](http://code.google.com/p/gstmanager) aims to ease starting a gstreamer-based project by wrapping most of the needed initialization requirements, with an orientation on string-based operation for live manipulation.

Based on the gstreamer python bindings, gstmanager offers the following helpers through the [PipelineManager](http://code.google.com/p/gstmanager/source/browse/trunk/gstmanager/gstmanager.py#17) class:
  * launch from pipeline description string ([example](http://code.google.com/p/gstmanager/source/browse/trunk/tests/test_gstmanager.py))
  * states wrapping
  * position/seeking wrapping
  * manual EOS emission
  * caps parsing
  * element message proxy (to very easy to use event system) ([example](http://code.google.com/p/gstmanager/source/browse/trunk/tests/test_messages.py))
  * negociated caps reporting ([example](http://code.google.com/p/gstmanager/source/browse/trunk/tests/test_caps_reporting.py))

Sub-projects:
  * [SBinManager](http://code.google.com/p/gstmanager/source/browse/trunk/tests/test_sbinmanager.py) (SBin for "String Bin"), is a gstreamer pipeline description string generator, with encoding profile support and examples source, sink, analysis and [encoding](http://code.google.com/p/gstmanager/source/browse/trunk/tests/test_ogg_fileencoder.py) SBins
  * [Detector](http://code.google.com/p/gstmanager/source/browse/trunk/tests/test_detector.py): physical input detection helpers

Deps:
  * python
  * gstreamer and python bindings
  * gtk python bindings (for the main loop)
  * [easyevent](https://launchpad.net/easyevent)