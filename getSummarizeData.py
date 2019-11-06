#!/usr/bin/env python
# (C) Copyright 2019-2020, PwC
#
# @brief Summarising the Full content using various algorithms

from framework.summarizeData.contentSummarization import contentSummarization
from framework.commonConstants import *
import pandas as pd
from os.path import join
from config import dataframeWithSummary, dataframeWithContent, encoderURL, rootDir

dfPath = join(rootDir, dataframeWithContent + PKL)
#dfPath = join(rootDir, dataframeWithSummary + PKL)

def getSummarizeData(dfPath, downloadPath, encoderURL, masterDataframeWithSummary):
    df = pd.read_pickle(dfPath)
    dataObject = contentSummarization(dataframe=df, encoderURL=encoderURL)
    df = contentSummarization.writingSummaryIntoDataframe1(dataObject)
    df.to_pickle(join(downloadPath, masterDataframeWithSummary + PKL))
    df = contentSummarization.writingSummaryIntoDataframe2(dataObject)
    df.to_pickle(join(downloadPath, masterDataframeWithSummary + PKL))

if __name__ == '__main__':
	getSummarizeData(dfPath=dfPath,
	                 downloadPath=rootDir,
	                 encoderURL=encoderURL,
	                 masterDataframeWithSummary=dataframeWithSummary)
