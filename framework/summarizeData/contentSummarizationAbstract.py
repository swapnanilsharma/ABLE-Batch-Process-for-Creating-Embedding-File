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

class contentSummarizationAbstract(ABC):
    __metaclass__ = ABCMeta

    # For extractContentDataSummarizationClass

    @abstractmethod
    def sentToVect(self, sentToEncode):
    	pass

    @abstractmethod
    def writingSummaryIntoDataframe1(self, numberOfSentences=10):
        pass

    @abstractmethod
    def writingSummaryIntoDataframe2(self, numOfSentences=10):
        pass

    @abstractmethod
    def writingSummaryIntoDataframe3(self, numOfSentences=10):
        pass
