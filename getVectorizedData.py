#!/usr/bin/env python
# (C) Copyright 2019-2020, PwC
#
# @brief vectorising content and content summary using Universal Sentence Encoder

from framework.dfToVector.dfColumnToVect import dfColumnToVect
from framework.commonConstants import *
import pandas as pd
from os.path import join
from config import dataframeWithSummary, rootDir, dataframeWithVector, encoderURL

dfPath = join(rootDir, dataframeWithSummary + PKL)

def readRawDataAddIntoDataframe(dfPath, encoderURL, downloadPath, vectorizedDataframe):
    df = pd.read_pickle(dfPath)
    dataObject = dfColumnToVect(dataframe=df,
		                        encoderURL=encoderURL)
    df = dfColumnToVect.contentToVector(dataObject)
    df = dfColumnToVect(dataframe=df, encoderURL=encoderURL).addKeywordVectorTodf()
    df.to_pickle(join(downloadPath, vectorizedDataframe + PKL))


if __name__ == '__main__':
	readRawDataAddIntoDataframe(dfPath=dfPath,
		                        encoderURL=encoderURL,
		                        downloadPath=rootDir,
		                        vectorizedDataframe=dataframeWithVector)
