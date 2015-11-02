#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

VERSION = "0.8"

setup(
    name="gstmanager",
    version=VERSION,
    description="gstmanager is a helper for building gstreamer applications",
    author="Florent Thiery",
    author_email="florent.thiery@ubicast.eu",
    url="http://code.google.com/p/gstmanager/",
    license="GNU/LGPLv3",
    packages=[
        'gstmanager',
        'gstmanager/detectors',
        'gstmanager/sbins',
        'gstmanager/sbins/encoders',
        'gstmanager/sbins/analysis',
        'gstmanager/sbins/sinks',
        'gstmanager/sbins/sources',
        'gstmanager/profiles'
    ],
    install_requires=[
        'python-easyevent',
        'python-gst0.10',
        'python-gobject',

    ]
)
