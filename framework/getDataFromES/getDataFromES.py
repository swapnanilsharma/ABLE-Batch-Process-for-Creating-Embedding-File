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

import pandas as pd
import warnings
import os
import requests
from pytube import YouTube
from os.path import isfile, join
from tqdm import tqdm
from framework.getDataFromES.getDataFromESAbstract import getDataFromESAbstract
from framework.commonConstants import *
from framework import commonLog
from framework import commonExceptions
from framework.subModule.channelClass import channelClass
from framework.subModule.ESOperationClass import ESOperationClass
from framework.getResponseFromCSApi import getResponseFromCSApi


# ****************************************************************************
# Constants
# ****************************************************************************

# ****************************************************************************
# Classes
# ****************************************************************************


class getDataFromES(getDataFromESAbstract):
    """docstring for extractRawDataFromESClass"""

    def __init__(self, dataframe, validChannelsName, validContentType = [RESOURCE, COLLECTION, COURSE]):
        """ Getting index of valid datapoint,
            i.e. for Content, Collection and Course
        """
        self.dataframe         = dataframe
        self.validChannelsName = validChannelsName
        self.validContentType  = validContentType

        if self.dataframe is None:
            raise commonExceptions.MandatoryParameterError('\'dataframe\' is mendatory parameter!!')
        if self.validChannelsName is None:
            raise commonExceptions.MandatoryParameterError('\'validChannelsName\' are mendatory parameter!!')


    def gettingValidDataPoints(self):

        validChannels = channelClass(dataframe=self.dataframe,
                                     channelNameList=self.validChannelsName).channelNameToChannelId()

        es_obj = ESOperationClass(dataframe = self.dataframe)
        self.dataPointCounter = es_obj.findValidResourceFromESCompositeSearchIndex(validChannels=validChannels)
        commonLog.log(f'Total Content, Collection and Course: {len(self.dataPointCounter)}')

    def gettingValidContentCollectionCourse(self):

        self.gettingValidDataPoints()
        es_obj = ESOperationClass(dataframe = self.dataframe)

        contentList, collectionList, courseList = es_obj.findingValidContentCollectionCourse(
            dataPointCounter=self.dataPointCounter)

        commonLog.log(f"----> Total Content    : {len(contentList)}")
        commonLog.log(f"----> Total Collection : {len(collectionList)}")
        commonLog.log(f"----> Total Course     : {len(courseList)}")

        return contentList, collectionList, courseList

    def gettingValidContent(self):
        contentList, collectionList, courseList = self.gettingValidContentCollectionCourse()
        es_obj = ESOperationClass(dataframe = self.dataframe)
        videoContent, pdataframe, ekstepContent = es_obj.findingValidContent(contentList=contentList)

        commonLog.log(f"---->----> Total Video  Content : {len(videoContent)}")
        commonLog.log(f"---->----> Total PDF    Content : {len(pdataframe)}")
        commonLog.log(f"---->----> Total EkStep Content : {len(ekstepContent)}")

        return videoContent, pdataframe, ekstepContent

    def __repr__(self):
        return f'{self.__class__.__name__}({self.compositeSearchJsonPath, self.validChannelsName})'

    def extractRawContent(self, downloadPath):
        """
        Downloading raw contents into specified path
        downloadPath: path where to download the files
        pdfDir, videoDir, ekstepDir: directories inside downloadPath
        """

        if not os.path.exists(join(downloadPath, pdfDir)):
            os.makedirs(join(downloadPath, pdfDir))
        if not os.path.exists(join(downloadPath, videoDir)):
            os.makedirs(join(downloadPath, videoDir))
        if not os.path.exists(join(downloadPath, ekstepDir)):
            os.makedirs(join(downloadPath, ekstepDir))

        videoContent, pdataframe, ekstepContent = self.gettingValidContent()

        # Extract PDF content
        for i in tqdm(pdataframe, desc='Downloading PDF contents'):
            source = self.dataframe[[ID, SOURCE]].loc[i].to_dict()[SOURCE]
            file_name = source[IDENTIFIER]
            r = requests.get(source[ARTIFACT_URL])
            with open(join(downloadPath,
                           pdfDir,
                           file_name + DOT + PDF), 'wb') as f:
                f.write(r.content)

        # Extract video content
        for i in tqdm(videoContent, desc='Downloading Video contents'):
            source = self.dataframe[[ID, SOURCE]].loc[i].to_dict()[SOURCE]
            file_name = source[IDENTIFIER]
            r = requests.get(source[ARTIFACT_URL])
            try:
                YouTube(source[ARTIFACT_URL]).streams.first().download(
                        output_path=join(downloadPath, videoDir),
                        filename=file_name)
            except:
                with open(join(downloadPath,
                               videoDir,
                               file_name + DOT + MP4), 'wb') as f:
                    f.write(r.content)

        # Extract ekstep content
        for i in tqdm(ekstepContent, desc='Downloading Ekstep contents'):
            self.source = self.dataframe[[ID, SOURCE]].loc[i].to_dict()[SOURCE]
            file_name = source[IDENTIFIER]
            r = requests.get(source[ARTIFACT_URL])
            with open(join(downloadPath,
                           ekstepDir,
                           file_name + DOT + ZIP), 'wb') as f:
                f.write(r.content)

    def buildMasterDataframe(self, apiUrl, taxonomyLevel, bearerToken, authId):
        """
        Building a dataframe for the valid Course, Collection and Content

        """
        additionalColumns = [LAST_UPDATE, MIMETYPE, CSRESPONSE, NAME, DESCRIPTION,
                             KEYWORDS, FULL_CONTENT, CONTENT_SUMMARY_1,
                             CONTENT_SUMMARY_2, CONTENT_SUMMARY_3]
        contentList, collectionList, courseList = self.gettingValidContentCollectionCourse()
        commonLog.log(f'contentList: {contentList}')
        commonLog.log(f'collectionList:{collectionList}')
        commonLog.log(f'courseList:{courseList}')
        columnsOfESJson = list(self.dataframe[[ID, SOURCE]].loc[self.dataPointCounter[0]].to_dict().keys())
        df = pd.DataFrame(columns = columnsOfESJson + additionalColumns)
        for idx, content in tqdm(enumerate(contentList)):
            df = df.append(self.dataframe[[ID, SOURCE]].loc[content].to_dict(), ignore_index=True)
            df[LAST_UPDATE].loc[idx] = self.dataframe[SOURCE].loc[content][LAST_UPDATE]
            df[MIMETYPE].loc[idx] = self.dataframe[SOURCE].loc[content][MIMETYPE]
            df[CSRESPONSE].loc[idx] = getResponseFromCSApi(apiUrl = apiUrl,
                                                           searchString = self.dataframe[ID].loc[content],
                                                           taxonomyLevel = taxonomyLevel,
                                                           bearerToken = bearerToken,
                                                           authId = authId)
            df[NAME].loc[idx] = self.dataframe[SOURCE].loc[content][NAME]
            try:
                df[DESCRIPTION].loc[idx] = self.dataframe[SOURCE].loc[content][DESCRIPTION]
            except KeyError:
                df[DESCRIPTION].loc[idx] = EMPTY
            try:
                df[KEYWORDS].loc[idx] = self.dataframe[SOURCE].loc[content][KEYWORDS]
            except KeyError:
                df[KEYWORDS].loc[idx] = EMPTY
        commonLog.log(f'DataFrame Created Successfully!!')
        return df
