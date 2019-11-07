#!/usr/bin/env python
# (C) Copyright 2019-2020, PwC
#
# @brief content search API's response

import requests
import pandas as pd
from framework.commonConstants import *

class getResponseFromCSApi():
    def __init__(self, apiUrl):
        self.apiUrl  = apiUrl
        self.headers = {'Content-Type' : APPLICATION_JSON, 'Cache-Control': NO_CACHE}

    def getResponseAgainstDoId(self, searchString):
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
        r = requests.post(url=self.apiUrl, json=data, headers=self.headers)
        if r.status_code == 200:
            return r.text
        else:
            return -1

    def generateContentJson(self, limit=1, mimeType=APPLICATION_PDF):
        data = {
          "request": {
             "filters": {"mimeType": mimeType},
             "limit"  : limit
          }
        }
        r = requests.post(url=self.apiUrl, json=data, headers=self.headers)
        if r.status_code == 200:
            return r.text
        else:
            return -1
