#!/usr/bin/env python
# ****************************************************************************
# (C) Copyright 2019-2020, PwC
#
# @ Class to extracting PDF content and text summarization
#
# ****************************************************************************

# ****************************************************************************
# Imports
# ****************************************************************************

import pandas as pd
import numpy as np
import warnings
from framework.dfToVector.dfColumnToVectAbstract import dfColumnToVectAbstract
from framework.commonConstants import *
import requests
import ast
from nltk import sent_tokenize

# ****************************************************************************
# Constants
# ****************************************************************************
# encoderURL = 'http://127.0.0.1:5456/encoder'

# ****************************************************************************
# Classes
# ****************************************************************************

class dfColumnToVect(dfColumnToVectAbstract):
    """docstring for convertDataframeColumnstoVectors"""

    def __init__(self, dataframe, encoderURL):

        """
        dataframe:
        """
        self.dataframe = dataframe
        self.encoderURL = encoderURL

    def __repr__(self):
        return f'{self.__class__.__name__}(dataframe, \'{self.dataframe}\', encoderURL, \'{self.encoderURL}\')'

    def sentToVect(self, sentToEncode):
        """ 512D sentence encoding using Universal Sentende Encoder """
        data = {'sentToEncode': [sentToEncode]}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url=self.encoderURL,
                          params=data,
                          headers=headers)
        if r.status_code == 200:
            output = ast.literal_eval(r.text)
        else:
            output = np.array(dOfVector*[0])
        return output

    def addVectorTodf(self, content, index, columnName):
        if not pd.isnull(content):
            contentVect = np.array(self.sentToVect(sent_tokenize(content)))
            self.dataframe[columnName].iloc[index] = np.sum(contentVect, axis=0)
        else:
            self.dataframe[columnName].iloc[index] = np.array(dOfVector*[0])

    def contentToVector(self):
        self.dataframe[FULL_CONTENT_VECTOR]      = EMPTY
        self.dataframe[CONTENT_SUMMARY_1_VECTOR] = EMPTY
        self.dataframe[CONTENT_SUMMARY_2_VECTOR] = EMPTY
        self.dataframe[CONTENT_SUMMARY_3_VECTOR] = EMPTY
        self.dataframe[NAME_VECTOR]              = EMPTY
        self.dataframe[DESCRIPTION_VECTOR]       = EMPTY

        for index, row in self.dataframe.loc[self.dataframe[MIMETYPE] == APPLICATION_PDF][[FULL_CONTENT, CONTENT_SUMMARY_1, CONTENT_SUMMARY_2, CONTENT_SUMMARY_3, NAME, DESCRIPTION]].iterrows():
            self.addVectorTodf(row[0], index, FULL_CONTENT_VECTOR)
            self.addVectorTodf(row[1], index, CONTENT_SUMMARY_1_VECTOR)
            self.addVectorTodf(row[2], index, CONTENT_SUMMARY_2_VECTOR)
            self.addVectorTodf(row[3], index, CONTENT_SUMMARY_3_VECTOR)
            self.addVectorTodf(row[4], index, NAME_VECTOR)
            self.addVectorTodf(row[5], index, DESCRIPTION_VECTOR)

        return self.dataframe

    def addKeywordVectorTodf(self):
        for idx in range(len(self.dataframe)):
            self.dataframe.loc[idx, KEYWORDS_VECTOR] = self.sentToVect(self.dataframe.loc[idx, KEYWORDS])
        return self.dataframe
