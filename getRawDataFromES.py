#!/usr/bin/env python
# (C) Copyright 2019-2020, PwC
#
# @brief extracting raw files from BLOB and make the basic dataframe

from framework.getDataFromES.getDataFromES import getDataFromES
from framework.commonConstants import *
import pandas as pd
from os.path import join
from config import rootDir, basicDataframe, apiUrl, contentJsonFileName, limit

def getRawDataFromES(downloadPath, masterDataframeName, apiUrl):
    dataObject = getDataFromES(apiUrl=apiUrl)
    '''
    dataObject.createJson(rootDir=rootDir,
                          contentJsonFileName=contentJsonFileName,
                          limit=limit,
                          mimeType=APPLICATION_PDF)
    '''
    contentList = pd.read_json(join(rootDir, contentJsonFileName)).loc['content', 'result']
    dataObject.extractRawContent(downloadPath=rootDir, contentList=contentList)

    df = dataObject.buildMasterDataframe(contentList=contentList)
    df.to_pickle(join(downloadPath, masterDataframeName + PKL))

if __name__ == '__main__':
	getRawDataFromES(downloadPath=rootDir,
	                 masterDataframeName=basicDataframe,
                     apiUrl=apiUrl)
