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

class dfColumnToVectAbstract(ABC):
    __metaclass__ = ABCMeta

    # For convertDataframeColumnstoVectors
    @abstractmethod
    def sentToVect(self, sentToEncode):
        pass

    @abstractmethod
    def contentToVector(self):
        pass

    @abstractmethod
    def addVectorTodf(self):
        pass

    @abstractmethod
    def addKeywordVectorTodf(self):
        pass
