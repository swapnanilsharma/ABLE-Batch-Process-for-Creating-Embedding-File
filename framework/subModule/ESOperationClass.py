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

class ESOperationClass(object):
    """docstring for elasticsearchOperationClass"""
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def findValidResourceFromESCompositeSearchIndex(self, validChannels, validContentType = [RESOURCE, COLLECTION, COURSE]):
        dataPointCounter = []
        for idx in range(len(self.dataframe)):
            source = self.dataframe[[ID, SOURCE]].loc[idx].to_dict()[SOURCE]
            try:
                if source[ATTR_CHANNEL] in validChannels and \
                   source[STATUS] == LIVE and \
                   source[FRAMEWORK] != NCF and \
                   source[CONTENT_TYPE] in validContentType and \
                   source[OBJECT_TYPE] in [CONTENT]:
                    # below are optional filters
                    if source[IDENTIFIER][0:3] == DO:
                        if source[IL_FUNC_OBJECT_TYPE] == CONTENT:
                            dataPointCounter.append(idx)
            except KeyError:
                pass
        return dataPointCounter

    def findingValidContentCollectionCourse(self, dataPointCounter):

        """ Getting Content, Collection and Course list index
        """
        contentList, collectionList, courseList = [], [], []
        for i in dataPointCounter:
            source = self.dataframe[[ID, SOURCE]].loc[i].to_dict()[SOURCE]
            if source[CONTENT_TYPE] == RESOURCE:
                contentList.append(i)
            elif source[CONTENT_TYPE] == COLLECTION:
                collectionList.append(i)
            elif source[CONTENT_TYPE] == COURSE:
                courseList.append(i)
        return contentList, collectionList, courseList

    def findingValidContent(self, contentList):

        """ Getting Types of content from content list """

        videoContent, pdfContent, ekstepContent = [], [], []
        for i in contentList:
            source = self.dataframe[[ID, SOURCE]].loc[i].to_dict()[SOURCE]
            if source[ARTIFACT_URL][-3:] == MP4 or \
               'www.youtube.com' in source[ARTIFACT_URL] or \
               'youtu.be' in source[ARTIFACT_URL]:
                videoContent.append(i)
            elif source[ARTIFACT_URL][-3:] == PDF:
                pdfContent.append(i)
            else:
                ekstepContent.append(i)
        return videoContent, pdfContent, ekstepContent