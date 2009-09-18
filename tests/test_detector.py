#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import logging, sys

    logging.basicConfig(
        level=getattr(logging, "DEBUG"),
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        stream=sys.stderr
    )

    sbins = []

    from gstmanager.detectors.alsa import AlsaDetector
    a = AlsaDetector()
    a.detect_devices()

    from gstmanager.sbins.sources.alsa import AlsaSource
    for device in a.devices_list:
        alsa_sbin = AlsaSource(device_id=device)
        sbins.append(alsa_sbin)

    from gstmanager.detectors.v4l import V4LDetector
    d_v4l = V4LDetector()
    d_v4l.detect_devices()

    from gstmanager.sbins.sources.v4l import V4LSource
    for device in d_v4l.devices_list:
        v4l_sbin = V4LSource(device_id=device)
        sbins.append(v4l_sbin)
        
    from gstmanager.detectors.firewire import FirewireDetector
    d_fire = FirewireDetector()
    d_fire.detect_devices()

    from gstmanager.sbins.sources.firewire import FirewireSource
    for device in d_fire.devices_list:
        fire_sbin = FirewireSource(device_id=device)
        sbins.append(fire_sbin)

    for sbin in sbins:
        print "Got %s %s, gstreamer source bin is: %s" %(sbin.type, sbin.description, sbin.sbin)
