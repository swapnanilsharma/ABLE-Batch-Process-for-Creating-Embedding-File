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

from framework.commonConstants import *
from framework import commonLog

class channelClass(object):
    """docstring for channelClass"""
    def __init__(self, dataframe, channelNameList=None, channelIdList=None):

        """
        channelNameList: channel names in list format; e.g. ['visakhapatnam', 'pcmc', 'nulp']
        channelIdList  : channel id in list format; e.g. ['01275318444026265621', '0127476715271127047']
        """
        self.dataframe       = dataframe
        self.channelNameList = channelNameList
        self.channelIdList   = channelIdList

        existChannel = []
        if self.channelNameList is not None:
            for cname in self.channelNameList:
                for dsource in self.dataframe[SOURCE]:
                    if dsource[OBJECT_TYPE] == VAL_CHANNEL and dsource[NAME] == cname:
                        existChannel.append(dsource[NAME])
            if set(channelNameList) - set(existChannel):
                commonLog.log(f'{list(set(channelNameList) - set(existChannel))} are not valid channel name!!')

        existChannel = []
        if self.channelNameList is not None:
            for cname in self.channelNameList:
                for dsource in self.dataframe[SOURCE]:
                    if dsource[OBJECT_TYPE] == VAL_CHANNEL and dsource[NAME] == cname:
                        existChannel.append(dsource[NAME])
            if set(channelNameList) - set(existChannel):
                commonLog.log(f'{list(set(channelNameList) - set(existChannel))} are not valid channel name!!')


    def channelNameToChannelId(self):
        return [idx[IDENTIFIER] for idx in list(self.dataframe[SOURCE].to_dict().values())
                         if idx[OBJECT_TYPE] == VAL_CHANNEL and
                         idx[NAME] in self.channelNameList]

    def channelIdToChannelName(self):
    	return [idx[NAME] for idx in list(self.dataframe[SOURCE].to_dict().values()) 
             if idx[OBJECT_TYPE] == VAL_CHANNEL and
                idx[IDENTIFIER] in self.channelIdList]

    def validateChannelNameId(self):
        if self.channelNameToChannelId() == self.channelIdList and \
           self.channelIdToChannelName() == self.channelNameList:
    	    return True
        else:
    	    return False

    def __repr__(self):
        return f'{self.__class__.__name__}({self.channelName, self.channelId})'
		