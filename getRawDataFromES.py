#!/usr/bin/env python
# (C) Copyright 2019-2020, PwC
#
# @brief extracting raw files from BLOB and make the basic dataframe

from framework.getDataFromES.getDataFromES import getDataFromES
from framework.commonConstants import *
import pandas as pd
from os.path import join
from config import ESCompositesearchPath, rootDir, basicDataframe, validChannelsName, apiUrl, taxonomyLevel, bearerToken, authId

def getRawDataFromES(ESCompositesearchPath, downloadPath, masterDataframeName, validChannelsName, apiUrl, taxonomyLevel, bearerToken, authId):
    df = pd.read_json(ESCompositesearchPath, lines=True)
    dataObject = getDataFromES(dataframe=df, validChannelsName=validChannelsName)

    getDataFromES.extractRawContent(dataObject, downloadPath=downloadPath)

    df = getDataFromES.buildMasterDataframe(dataObject, apiUrl, taxonomyLevel, bearerToken, authId)
    df.to_pickle(join(downloadPath, masterDataframeName + PKL))


if __name__ == '__main__':
	getRawDataFromES(ESCompositesearchPath=ESCompositesearchPath,
	                 downloadPath=rootDir,
	                 masterDataframeName=basicDataframe,
	                 validChannelsName=validChannelsName,
                     apiUrl=apiUrl,
                     taxonomyLevel=taxonomyLevel,
                     bearerToken=bearerToken,
                     authId=authId)
