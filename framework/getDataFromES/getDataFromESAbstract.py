#!/usr/bin/env python
# ****************************************************************************
# (C) Copyright 2019-2020, PwC
#
# @ Class to extracting data from ElasticSearch Database
#
# ****************************************************************************

# ****************************************************************************
# Imports
# ****************************************************************************

from abc import ABC, ABCMeta, abstractmethod

# ****************************************************************************
# Constants
# ****************************************************************************

# ****************************************************************************
# Classes
# ****************************************************************************

class getDataFromESAbstract(ABC):
    __metaclass__ = ABCMeta

    # For extractRawDataFromESClass
    @abstractmethod
    def extractRawContent(self, downloadPath, pdfDir, videoDir, ekstepDir):
        pass

    @abstractmethod
    def buildMasterDataframe(self):
        pass
