#!/usr/bin/env python
# (C) Copyright 2019-2020, PwC
#
# @brief configuration file for NLP Search Framework
from os.path import join

coreDBPublicIP        = '52.230.69.130'
kpDBPrivateIP         = '80.1.0.9'

#ESCompositesearchPath = "C:/Users/Swapnanil/Machine Learning/PwC/Elastic Data from NUIS/compositesearch_new.json"
#rootDir               = 'C:/PWC/PWC'
#validChannelsName     = ['visakhapatnam', 'pcmc', 'nulp']
ESCompositesearchPath = "C:/PWC/devNULP/devNULP/devNULPcomposite.json"
rootDir               = 'C:/PWC/devNULP/devNULP'
validChannelsName     = ['nuis', 'advisory', 'pwc_test2', 'channel25july', 'nulp', 'niua',
                         'advisory1', 'pcmc', 'pwc_test3', 'pwc_test', 'pwc_test1', 'mankind', 'tax']

# Code for get channalNames
# [idx['name'] for idx in list(df_content['_source'].to_dict().values()) if idx['objectType'] == 'Channel'] #identifier
basicDataframe        = 'basicDataframe'
dataframeWithContent  = 'dataframeWithContent'
dataframeWithSummary  = 'dataframeWithSummary'
dataframeWithVector   = 'dataframeWithVector'
dataframeFinal        = 'dataframeFinalServer512D'

encoderURL            = 'http://127.0.0.1:5456/encoder'

# parameters for calling 'api.content.search' API
apiUrl        = 'https://devnulp.nuis.in/api/content/v1/search'
taxonomyLevel = ['board', 'gradeLevel', 'subject', 'medium']
bearerToken   = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIxOTA3MDY0MGY5MTI0YzMyOWZjY2I2MWYwNTQ2M2RkYyJ9.4_wwo6J5QgwdQaOPSlqh0iHOAFwWNlVWY_syit3DDGQ'
authId        = 'Not mandatory'
