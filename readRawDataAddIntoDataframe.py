#!/usr/bin/env python
# (C) Copyright 2019-2020, PwC
#
# @brief Extract texts from downloaded content and put them into the dataframe

from framework.readData.readFullData import readFullData
from framework.commonConstants import *
import pandas as pd
from os.path import join
from config import rootDir, basicDataframe, dataframeWithContent

dfPath = join(rootDir, basicDataframe + PKL)

def readRawDataAddIntoDataframe(dfPath, downloadPath, masterDataframeWithContent):
    df = pd.read_pickle(dfPath)
    dataObject = readFullData(dataframe=df, downloadPath=downloadPath)
    df = readFullData.populatingFullContentForPDF(dataObject)
    df.to_pickle(join(downloadPath, masterDataframeWithContent + PKL))


if __name__ == '__main__':
	readRawDataAddIntoDataframe(dfPath=dfPath,
		                        downloadPath=rootDir,
                                masterDataframeWithContent=dataframeWithContent)
