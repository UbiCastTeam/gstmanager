#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger("encoder")

import datetime
from gstmanager.profile import DefaultEncodingProfile
from gstmanager.event import EventLauncher, EventListener

class ProgressInfo(EventListener):
    def __init__(self):
        EventListener.__init__(self)
        self.start_time = datetime.datetime.now()
        self.hduration = "0:00:00"
        self.size = 0
        self.registerEvent("sos")

    def update(self, size):
        self.size = size
        self.duration = dur = datetime.datetime.now() - self.start_time
        self.hduration = str(dur).split(".")[0]

    def evt_sos(self, event):
        self.start_time = datetime.datetime.now()
        self.size = 0

class AudioEncoder(object):
    index = 0
    def __init__(self, sbin_content):
        self.tags = ["a_src_tee"]
        self.enc_tag = "a_enc_%s_tee" %AudioEncoder.index
        sbin_begin = "%s. ! queue ! audioconvert !" %self.tags[0]
        sbin_end = "! queue ! tee name=%s" %(self.enc_tag)
        self.sbin = "%s %s name=aencoder_%s %s" %(sbin_begin, sbin_content, AudioEncoder.index, sbin_end)
        AudioEncoder.index += 1

class VideoEncoder(object):
    index = 0
    def __init__(self, sbin_content, profile=DefaultEncodingProfile()):
        self.profile = profile
        self.tags = ["v_src_tee"]
        self.enc_tag = "v_enc_%s_tee" %VideoEncoder.index
        self.caps = "video/x-raw-yuv, format=(fourcc)I420, width=(int)%s, height=(int)%s, framerate=(fraction)25/1" %(profile.video_width, profile.video_height)
        sbin_begin = "%s. ! queue ! ffmpegcolorspace ! videorate ! videoscale ! %s !" %(self.tags[0], self.caps)
        sbin_end = "! queue ! tee name=%s" %self.enc_tag
        self.sbin = "%s %s name=vencoder_%s %s" %(sbin_begin, sbin_content, VideoEncoder.index, sbin_end)
        VideoEncoder.index += 1

from gstmanager.sbinmanager import SBinManager
import gobject, os

class FileEncoder(SBinManager, EventLauncher, EventListener):
    def __init__(self, filename):
        SBinManager.__init__(self)
        EventListener.__init__(self)
        EventLauncher.__init__(self)
        self.progress = ProgressInfo() 
        self.check_for_compat = False
        self.filename = filename
        self.size = 0
        self.is_running = False
        self.registerEvent("sos")
        self.registerEvent("eos")

    def destroy(self):
        logger.debug("Unregistering event sos")
        self.unregisterEvent("sos")
        self.size = 0

    def get_filename(self):
        return self.filename

    def get_filesize(self):
        filename = self.get_filename()
        if os.path.isfile(filename):
            return os.path.getsize(filename)
        else:
            logger.error("File %s does not exist" %filename)
            return 0

    def evt_sos(self, event):
        logger.info("SOS: Starting filesize checking")
        self.is_running = True
        gobject.timeout_add(1000, self.check_file_growth)

    def evt_eos(self, event):
        logger.info("EOS: Stopping filesize checking")
        self.is_running = False
        self.size = 0

    def check_file_growth(self):
        new_size = self.get_filesize()
        logger.debug("Current file size is %s" %new_size)
        if new_size <= self.size and self.is_running:
            logger.error("File %s growth stalled !" %self.filename)
            self.launchEvent("encoding_error", "Encoding of %s stopped" %self.filename)
            return False
        elif not self.is_running:
            return False
        elif self.is_running:
            self.progress.update(new_size)
            self.launchEvent("encoding_progress", self.progress)            
            return True
