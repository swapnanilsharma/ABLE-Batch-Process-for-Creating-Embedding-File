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
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os
import shutil
from os.path import isfile, join
from tqdm import tqdm
from datetime import datetime
from nltk.tokenize import sent_tokenize, word_tokenize
import spacy
import re
import operator
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import flask
import requests
import ast
import simplejson as json
from nltk.corpus import stopwords
from math import ceil
from framework.readData.readFullDataAbstract import readFullDataAbstract
from framework.commonConstants import *
from framework.subModule.dataFilterMethod import *
from framework import commonLog


# ****************************************************************************
# Constants
# ****************************************************************************
TEMP = 'temp_'
OUTDIR = 'outDir'
PAGE = 'page_'
DPI = 200
NO_OF_THREADS = 4
MAX_WORD_LENGTH = 45
MAX_VALID_SENTENCE_LENGTH = 200
MIN_VALID_SENTENCE_LENGTH = 6
TESSERACT_PATH = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
spacy_nlp = spacy.load('en_core_web_md')
# ****************************************************************************
# Classes
# ****************************************************************************


class readFullData(readFullDataAbstract):
    """docstring for extractContentDataClass"""

    def __init__(self, dataframe, downloadPath):

        """
        dataframe: dataframe where need to store the extracted texts
        downloadPath: path where raw pdf files are stored
        pdfDir: directory inside downloadPath

        """
        self.dataframe = dataframe
        self.downloadPath = downloadPath

    def __repr__(self):
        return f'{self.__class__.__name__}(dataframe, \'{self.downloadPath}\')'

    def populatingFullContentForPDF(self):

        """
        Populating 'Full Content' column of the dataframe from raw content using Tesseract-OCR
        """

        # CHANGE THIS IF TESSERACT IS NOT IN YOUR PATH, OR IS NAMED DIFFERENTLY
        # pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

        paths = [f for f in os.listdir(join(self.downloadPath, pdfDir)) if isfile(join(self.downloadPath, pdfDir, f))]

        for pdfFile in tqdm(paths, desc='Extracting PDF file\'s content'):
            # Create a temporary directory
            dirName = TEMP + pdfFile[:-4]
            outDir = OUTDIR
            if not os.path.exists(join(self.downloadPath, pdfDir, outDir)):
                os.mkdir(join(self.downloadPath, pdfDir, outDir))
            else:
                pass
            if not os.path.exists(join(self.downloadPath, pdfDir, dirName)):
                os.mkdir(join(self.downloadPath, pdfDir, dirName))
            else:
                pass
            pages = convert_from_path(join(self.downloadPath, pdfDir, pdfFile), dpi=DPI,
                                      first_page=None, last_page=None, thread_count=NO_OF_THREADS,
                                      output_folder=join(self.downloadPath, pdfDir, outDir))
            image_counter = 1
            for page in pages:
                filename = PAGE + str(image_counter) + '.' + JPG
                page.save(join(self.downloadPath, pdfDir, dirName, filename), 'JPEG')
                image_counter = image_counter + 1
            filelimit = image_counter-1
            outfile = pdfFile[:-4] + '.' + TXT
            f = open(join(self.downloadPath, pdfDir, dirName, outfile), "a")
            for i in range(1, filelimit + 1):
                filename = PAGE + str(i) + '.' + JPG
                try:
                    text = str(((pytesseract.image_to_string(Image.open(join(self.downloadPath, pdfDir, dirName, filename))))))
                    text = text.replace('-\n', '')
                    f.write(text)
                except:
                    commonLog.log(f"file: {pdfFile} has issue in page number: {i}")
            f.close()
            f = open(join(self.downloadPath, pdfDir, dirName, outfile), "r")
            fileOut = f.read()
            f.close()
            try:
                shutil.rmtree(join(self.downloadPath, pdfDir, outDir), ignore_errors=True)
            except PermissionError:
                pass

            try:
                shutil.rmtree(join(self.downloadPath, pdfDir, dirName), ignore_errors=True)
            except PermissionError:
                pass
            idx = self.dataframe.loc[self.dataframe[ID] == pdfFile[:-4]].index.tolist()[0]
            full_cont = ' '.join(self.preprocessingOfFullContent(fileOut))
            self.dataframe.iloc[idx, self.dataframe.columns.get_loc(FULL_CONTENT)] = full_cont
        return self.dataframe

    def populatingFullContentForVideo(self):
        pass

    def populatingFullContentForEkstepContent(self):
        pass

    @staticmethod
    def preprocessingOfFullContent(fullContent):
        validSentences = findValidSentences(fullContent)
        validSentences = [expandContractions(i) for i in validSentences]
        validSentences = [re.sub('\n', '', i) for i in validSentences]
        return validSentences