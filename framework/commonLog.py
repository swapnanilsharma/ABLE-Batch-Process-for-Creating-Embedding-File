#!/usr/bin/env python
# (C) Copyright 2019-2020, PwC
#
# @brief constants used by NLP Search Framework
#
#****************************************************************************

#****************************************************************************
# Imports
#****************************************************************************
import time, logging


#****************************************************************************
# Constants
#****************************************************************************

DEFAULT_LOG_FILE = None

LOG_LEVEL_ERROR = 1
LOG_LEVEL_DEBUG = 2
LOG_LEVEL_TRACE = 3
LOG_LEVEL_ALWAYS = 4
LOG_LEVEL_DEFAULT = LOG_LEVEL_ALWAYS

FIRST_LINE = ">>>>> NLP Engine LOG >>>>>\n"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

#****************************************************************************
# Global Variables
#****************************************************************************

file_handle = None
log_level = LOG_LEVEL_DEFAULT

#****************************************************************************
# Functions
#****************************************************************************


def open_log(log_file=DEFAULT_LOG_FILE, level=LOG_LEVEL_DEFAULT):
    global file_handle
    global log_level
    if log_file is not None:
        file_handle = open(log_file, "w")
        file_handle.write(FIRST_LINE)
    else:
        file_handle = None
    log_level = level

def close_log():
    global file_handle
    if file_handle is not None:
        file_handle.close()
        file_handle = None

def log(message, level=LOG_LEVEL_DEFAULT):
    global log_level
    global file_handle
    if level <= log_level or level == LOG_LEVEL_ALWAYS:
        current_time = time.strftime(DATETIME_FORMAT, time.localtime())
        out_str = "%s: %s\n" % (current_time, message)
        # this message meets our logging threshold.  log it
        if file_handle is not None:
            file_handle.write(out_str)
        else:
            print(out_str)


def set_log_level(new_level=LOG_LEVEL_DEFAULT):
    global log_level
    log_level = new_level
