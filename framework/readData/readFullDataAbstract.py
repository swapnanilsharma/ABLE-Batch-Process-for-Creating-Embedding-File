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

class readFullDataAbstract(ABC):
	__metaclass__ = ABCMeta

    # For extractContentDataSummarizationClass
	@abstractmethod
	def populatingFullContentForPDF(self):
		pass

	@abstractmethod
	def populatingFullContentForVideo(self):
		pass

	@abstractmethod
	def populatingFullContentForEkstepContent(self):
		pass
