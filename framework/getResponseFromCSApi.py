#!/usr/bin/env python
# (C) Copyright 2019-2020, PwC
#
# @brief content search API's response

import requests
import pandas as pd
from framework.commonConstants import *

def getResponseFromCSApi(apiUrl, searchString, taxonomyLevel, bearerToken, authId):
    headers = {'Content-Type'          : APPLICATION_JSON,
               'Authorization'         : bearerToken,
               'X-Authenticated-Userid': authId}
    data = {
      "request": {
         "filters": {
                     "status"     : [LIVE],
                     "channel"    : DUMMY_CHANNEL,
                     "board"      : [DUMMY_BOARD],
                     "contentType": [COLLECTION, TEXTBOOK, LESSONPLAN, RESOURCE],
                     },
         "limit"  : 20,
         "query"  : searchString,
         "softConstraints": {
                             "badgeAssertions" : 98,
                             "board"           : 99,
                             "channel"         : 100
                             },
         "mode"  :"soft",
         "facets": taxonomyLevel,
         "offset": 0
      }
    }
    r = requests.post(url=apiUrl, json=data, headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return -1
