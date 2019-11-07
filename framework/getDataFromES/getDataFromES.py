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

    def __init__(self, apiUrl):
        self.apiUrl = apiUrl

    def __repr__(self):
        return f'{self.__class__.__name__}(apiUrl={self.apiUrl})'

    def extractRawContent(self, downloadPath, contentList):
        """
        Downloading raw contents into specified path
        downloadPath: path where to download the files
        pdfDir, videoDir, ekstepDir: directories inside downloadPath
        """

        if not os.path.exists(join(downloadPath, pdfDir)):
            os.makedirs(join(downloadPath, pdfDir))

        # Extract PDF content
        for content in tqdm(contentList, desc='Downloading PDF contents'):
            file_name = content[IDENTIFIER]
            if not os.path.isfile(join(downloadPath, pdfDir, file_name + DOT + PDF)):
                r = requests.get(content[ARTIFACT_URL])
                with open(join(downloadPath, pdfDir, file_name + DOT + PDF), 'wb') as f:
                    f.write(r.content)

    def buildMasterDataframe(self, contentList, downloadPath, masterDataframeName):
        """
        Building a dataframe for the English PDF Content

        """
        if not os.path.isfile(join(downloadPath, masterDataframeName)):
            dfColumns = [ID, SOURCE, MEDIUM, LAST_UPDATE, MIMETYPE, CSRESPONSE, NAME, DESCRIPTION, KEYWORDS,
                         FULL_CONTENT, CONTENT_SUMMARY_1, CONTENT_SUMMARY_2, CONTENT_SUMMARY_3]
            df = pd.DataFrame(columns = dfColumns)
            for idx, content in tqdm(enumerate(contentList)):
                try:
                    df.loc[idx, MEDIUM] = content[MEDIUM]
                except KeyError:
                    df.loc[idx, MEDIUM] = EMPTY
                try:
                    df.loc[idx, ID] = content[IDENTIFIER]
                except KeyError:
                    df.loc[idx, ID] = EMPTY
                try:
                    df.loc[idx, LAST_UPDATE] = content[LAST_UPDATE]
                except KeyError:
                    df.loc[idx, LAST_UPDATE] = EMPTY
                try:
                    df.loc[idx, MIMETYPE] = content[MIMETYPE]
                except KeyError:
                    df.loc[idx, MIMETYPE] = EMPTY
                try:
                    df.loc[idx, NAME] = content[NAME]
                except KeyError:
                    df.loc[idx, NAME] = EMPTY
                try:
                    df.loc[idx, DESCRIPTION] = content[DESCRIPTION]
                except KeyError:
                    df.loc[idx, DESCRIPTION] = EMPTY
                try:
                    df.loc[idx, KEYWORDS] = content[KEYWORDS]
                except KeyError:
                    df.loc[idx, KEYWORDS] = EMPTY
                try:
                    df.loc[idx, SOURCE] = repr(content)
                except KeyError:
                    df.loc[idx, SOURCE] = EMPTY
                try:
                    df.loc[idx, CSRESPONSE] = getResponseFromCSApi(apiUrl = self.apiUrl).getResponseAgainstDoId(searchString = repr(content[IDENTIFIER]))
                except KeyError:
                    df.loc[idx, CSRESPONSE] = EMPTY

            commonLog.log(f'DataFrame Created Successfully at {join(downloadPath, masterDataframeName)}!!')
            df.to_pickle(join(downloadPath, masterDataframeName))
        else:
            commonLog.log(f'DataFrame already exist at {join(downloadPath, masterDataframeName)}!!')

    def createJson(self, rootDir, contentJsonFileName, limit=1, mimeType=APPLICATION_PDF):
        try:
            if not os.path.isfile(join(rootDir, contentJsonFileName)):
                jsonResp = getResponseFromCSApi(apiUrl = self.apiUrl).generateContentJson(limit=limit, mimeType=mimeType)
                f = open(join(rootDir, contentJsonFileName), 'w' )
                f.write((jsonResp))
                f.close()
                commonLog.log(f'Json file has been downloaded and saved at {join(rootDir, contentJsonFileName)}')
            else:
                commonLog.log(f'Json file is already downloaded at {join(rootDir, contentJsonFileName)}')
        except:
            commonLog.log(f'Json file downloaded process failed!')
