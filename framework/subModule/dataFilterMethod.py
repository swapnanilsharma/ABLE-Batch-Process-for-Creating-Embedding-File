#!/usr/bin/env python
# ****************************************************************************
# (C) Copyright 2019-2020, PwC
#
# @ Text Preprocessing Methods
#
# ****************************************************************************

# ****************************************************************************
# Imports
# ****************************************************************************

import pandas as pd
import numpy as np
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
import ast
import simplejson as json
from nltk.corpus import stopwords
from framework.commonConstants import *

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


def removeAbbriviationFromString(sentence):
    """
    Data cleaning method for sentences which are having abbriviations
    """
    # Removing words which are having more than 2 consecutive same letter
    sentConstruct = []
    for word in word_tokenize(sentence):
        if re.search(r'c{3}|e{3}|s{3}|r{3}|a{3}|\.{3}', word) or \
           len(word) > MAX_WORD_LENGTH or \
           len(word) > 2.5 * len(set(word)):  # if word has more repeating letters
            pass
        else:
            sentConstruct.append(word)
    sentence = ' '.join(sentConstruct)
    sentence = sentence.replace("i.e.", "in other words").replace("¢", "").replace("\n\n", '\n').replace("\n", ' ')
    for abv in list(ABBV_DICT.keys()):
        subWord = ""
        if re.search(re.escape(abv) + r"\.\s*[a-z0-9]", sentence):
            subWord = re.search(re.escape(abv) + r"\.\s*[a-z0-9]", sentence).group(0)[-1]
        sentence = re.sub(re.escape(abv) + r"\.\s*[a-z0-9]", ABBV_DICT[abv] + " " + subWord, sentence)
    sentence = sentence.replace("sq.", "square.").replace("km.", "kilometer.").replace("abbr.", "abbreviation")
    sentence = sentence.replace("cm.", "centimeter.").replace("etc.", "etc.").replace("Rs.", "Rupees.").replace("Rs .", "Rupees.")
    sentence = sentence.replace("kms.", "kilometeres.").replace("squarekms.", "square kilometeres.").replace("No.", "Number.")
    sentence = sentence.replace("squarem.", "square meter.").replace("eg.", "example.").replace("Pvt.", "Private.")
    sentence = sentence.replace("no.", "number.").replace("mt.", "meter.").replace("squareft.", "square feet.")
    sentence = sentence.replace("Ltd.", "Limited.").replace("NOS.", "Numbers.").replace("dt.", "dated.")
    sentence = sentence.replace("Ltrs.", "Liters.").replace("nos.", "nos.").replace("Tel.", "Telephone.")
    sentence = sentence.replace("Ms.", "Ms").replace("Mr.", "Mr").replace('Telephone.', 'Telephone:')
    sentence = sentence.replace('no .', 'number').replace('No .', 'Number')
    sentence = re.sub(r'\.\s*(Telephone)', ' Telephone', sentence)
    sentence = re.sub(r'\s', ' ', sentence)
    sentence = re.sub("[^a-zA-Z0-9\.@%&,:]", " ", sentence)
    sentence = re.sub(r'\d+\.\d+', '', sentence)
    sentence = re.sub(r'\d+\:\d+', '', sentence)
    return sentence


def expandContractions(sentence, contractions_dict=CONTRACTIONS):
    contractions_re = re.compile('(%s)' % '|'.join(contractions_dict.keys()))

    def replace(match):
        return contractions_dict[match.group(0)]
    return contractions_re.sub(replace, sentence)


def findValidSentences(sentences):
    """
    Finding ralevant sentences from the content
    """
    sentences = sent_tokenize(removeAbbriviationFromString(sentences))
    validSentences = []
    for i in range(len(sentences)):
        lenOfSent = len(word_tokenize(sentences[i]))
        if lenOfSent >= MIN_VALID_SENTENCE_LENGTH and lenOfSent <= MAX_VALID_SENTENCE_LENGTH:
            validSentences.append(sentences[i])
    return validSentences