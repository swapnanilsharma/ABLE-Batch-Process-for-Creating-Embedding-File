#!/usr/bin/env python
# (C) Copyright 2019-2020, PwC
#
# @brief final dataframe building

import numpy as np
import pandas as pd
from framework.commonConstants import *
from config import rootDir, dataframeWithVector, dataframeFinal
from os.path import join

dfPath = join(rootDir, dataframeWithVector + PKL)

def updateDF(index, content, dataframe):
    colList = [FULL_CONTENT_VECTOR, CONTENT_SUMMARY_1_VECTOR, CONTENT_SUMMARY_2_VECTOR,
               CONTENT_SUMMARY_3_VECTOR, NAME_VECTOR, DESCRIPTION_VECTOR]
    for col in colList:
        try:
            if content[col] == 0:
                dataframe.loc[index][col] = np.array(dOfVector*[0])
        except:
            pass
    return dataframe
    

if __name__ == '__main__':
    df = pd.read_pickle(dfPath)
    for idx, content in df.iterrows():
        df = updateDF(index=idx,
        	          content=content,
        	          dataframe=df)
    df.to_pickle(join(rootDir, dataframeFinal + PKL))

