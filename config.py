#!/usr/bin/env python
# (C) Copyright 2019-2020, PwC
#
# @brief configuration file for NLP Search Framework
from os.path import join

# parameters for calling 'api.content.search' API
apiUrl                = 'https://preprod.ntp.net.in/api/content/v1/search'
rootDir               = "C:/PWC/devNULP/diksha"
contentJsonFileName   = "completeJsonSwap.json"
limit                 = 10

# Code for get channalNames
# [idx['name'] for idx in list(df_content['_source'].to_dict().values()) if idx['objectType'] == 'Channel'] #identifier
basicDataframe        = 'basicDataframe'
dataframeWithContent  = 'dataframeWithContent'
dataframeWithSummary  = 'dataframeWithSummary'
dataframeWithVector   = 'dataframeWithVector'
dataframeFinal        = 'dataframeFinalServer512D'

encoderURL            = 'http://127.0.0.1:5456/encoder'
