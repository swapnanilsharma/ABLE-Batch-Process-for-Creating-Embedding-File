#!/usr/bin/env python
# ****************************************************************************
# (C) Copyright 2019-2020, PwC
#
# @ Class for text summarization
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
import operator
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import flask
import requests
import ast
import simplejson as json
from nltk.corpus import stopwords
from math import ceil
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

from framework.summarizeData.contentSummarizationAbstract import contentSummarizationAbstract
from framework.commonConstants import *
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
stop_words = set(stopwords.words("english"))
#encoderURL = 'http://127.0.0.1:5456/encoder'
# ****************************************************************************
# Classes
# ****************************************************************************


class contentSummarization(contentSummarizationAbstract):
    """docstring for extractContentDataSummarizationClass"""

    def __init__(self, dataframe, encoderURL):

        """
        dataframe: dataframe where need to store the extracted texts
        downloadPath: path where raw pdf files are stored
        pdfDir: directory inside downloadPath

        """
        self.dataframe = dataframe
        self.encoderURL = encoderURL

    def __repr__(self):
        return f'{self.__class__.__name__}(dataframe, \'{self.dataframe}\', encoderURL, \'{self.encoderURL}\')'

    #Most frequently occuring n-grams
    def getTopNNgramWords(self, corpus, ngram, n=10):
        vec1 = CountVectorizer(ngram_range=(ngram,ngram), max_features=2000).fit(corpus)
        bag_of_words = vec1.transform(corpus)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec1.vocabulary_.items()]
        words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
        return words_freq[:n]

    def getKeywords(self, rowName, newRowName, noOfWords=20):
        corpus = []
        for i in range(0, len(self.dataframe.loc[:, rowName])):
            if not pd.isnull(self.dataframe.loc[i, 'Full Content']):
                #Remove punctuations
                text = re.sub('[^a-zA-Z]', ' ', self.dataframe.loc[i, FULL_CONTENT])
                #Convert to lowercase
                text = text.lower()
                #remove tags
                text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ", text)
                # remove special characters and digits
                text=re.sub("(\\d|\\W)+"," ", text)
                ##Convert to list from string
                text = text.split()
                ##Stemming
                ps=PorterStemmer()
                #Lemmatisation
                lem = WordNetLemmatizer()
                text = [lem.lemmatize(word) for word in text if not word in stop_words]
                text = [" ".join(text)]
                top1_words = self.getTopNNgramWords(corpus=text, ngram=1, n=noOfWords)
                top2_words = self.getTopNNgramWords(corpus=text, ngram=2, n=noOfWords)
                top3_words = self.getTopNNgramWords(corpus=text, ngram=3, n=noOfWords)
                top4_words = self.getTopNNgramWords(corpus=text, ngram=4, n=noOfWords)
                if type(self.dataframe.loc[i, KEYWORDS]) == list:
                    all_keywords = (list(word[0] for word in top1_words) +
                                    list(word[0] for word in top2_words) +
                                    list(word[0] for word in top3_words) +
                                    list(word[0] for word in top4_words) +
                                    self.dataframe.loc[i, KEYWORDS])
                    corpus.append(list(set([i for i in all_keywords if not any(set(i) < set(j) for j in all_keywords)])))
                else:
                    all_keywords = (list(word[0] for word in top1_words) +
                                    list(word[0] for word in top2_words) +
                                    list(word[0] for word in top3_words) +
                                    list(word[0] for word in top4_words))
                    corpus.append(list(set([i for i in all_keywords if not any(set(i) < set(j) for j in all_keywords)])))
            else:
                corpus.append(np.nan)
        self.dataframe[newRowName] = corpus
        return self.dataframe

    def generatingKeywords(self):
        self.dataframe = self.getKeywords(rowName=FULL_CONTENT, newRowName=KEYWORDS, noOfWords=20)
        return self.dataframe

    def sentToVect(self, sentToEncode):
        """ 512D sentence encoding using Universal Sentende Encoder """
        data = {'sentToEncode': sentToEncode}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url=self.encoderURL, params=data, headers=headers)
        if r.status_code == 200:
            output =  np.asarray(ast.literal_eval(r.text)) # ast.literal_eval(r.text)
        else:
            output = np.asarray(-1)
        return output

    def writingSummaryIntoDataframe1(self, numberOfSentences=10):
        """
        Text Summarization: Sentence Scoring based on Word Frequency
        """
        for idx, fullContent in tqdm(self.dataframe.loc[self.dataframe[MIMETYPE] == APPLICATION_PDF][FULL_CONTENT].iteritems(),
                                     desc="Generating Summary1"):
            if not pd.isnull(fullContent) and len(fullContent) > 0:
                if len(fullContent) > 0:# and idx not in [0,2]:
                    #commonLog.log(f'======>>>>>> {idx}-->{len(fullContent)}')
                    validSentences = sent_tokenize(fullContent)
                    freq_table = self.createFreqTable(" ".join(validSentences))
                    sentence_scores = self.scoreSentences(validSentences, freq_table)
                    threshold = self.findAverageScore(sentence_scores)
                    summary1 = self.generateSummaryBasedOnSentenceScore(sentence_scores, 1.0 * threshold, numberOfSentences)
                    self.dataframe.iloc[idx, self.dataframe.columns.get_loc(CONTENT_SUMMARY_1)] = summary1
        return self.dataframe

    def writingSummaryIntoDataframe2(self, numOfSentences=10, subsetSize = 500):
        """ Text Summarization: TextRank using Universal Sentence Encoder """
        for idx, fullContent in tqdm(self.dataframe.loc[self.dataframe[MIMETYPE] == APPLICATION_PDF][FULL_CONTENT].iteritems(),
                                     desc="Generating Summary2"):
            if not pd.isnull(fullContent) and len(fullContent) > 0:
                if len(fullContent) > numOfSentences:
                    validSentences = sent_tokenize(fullContent)
                    summary2 = []
                    for i in range(ceil(len(validSentences)/subsetSize)):
                        messageEmbeddings = self.sentToVect(validSentences[i*subsetSize:(i+1)*subsetSize])
                        # generate cosine similarity matrix
                        sim_matrix = cosine_similarity(messageEmbeddings)
                        # create graph and generate scores from pagerank algorithms
                        nx_graph = nx.from_numpy_array(sim_matrix)
                        scores = nx.pagerank(nx_graph)
                        ranked_sentences = sorted(((scores[j], s) for j, s in enumerate(validSentences[i*subsetSize:(i+1)*subsetSize])), reverse=True)
                        summary2.append(" ".join([i[1] for i in ranked_sentences[:numOfSentences]]))
                    self.dataframe.iloc[idx, self.dataframe.columns.get_loc(CONTENT_SUMMARY_2)] = " ".join(i for i in summary2)
            else:
                self.dataframe.iloc[idx, self.dataframe.columns.get_loc(CONTENT_SUMMARY_2)] = ''
        return self.dataframe

    def writingSummaryIntoDataframe3(self, numOfSentences=10):
        pass


    @staticmethod
    def createFreqTable(sentences):
        """
        Finding frequency of words appeared in a text corpus
        """
        stopwords_list = set(stopwords.words('english'))
        words = word_tokenize(sentences)
        freqTable = {}
        for word in words:
            # lemmatize word
            for token in spacy_nlp(word):
                word = token.lemma_
            # remove stopwords
            if word in stopwords_list:
                continue
            elif word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1
        key_to_remove = []
        for key in freqTable.keys():
            if len(key) == 1:
                key_to_remove.append(key)
        for key in key_to_remove:
            freqTable.pop(key, None)
        return freqTable

    @staticmethod
    def scoreSentences(sentences, freqTable):
        """
        Calculating Ranking of the sentences from a text corpus:
        sentences having more frequent words will get high score
        """
        sentenceValue = {}
        for sentence in sentences:
            sentence = re.sub(r'\d+?', '', sentence)
            tempSent = ''
            for token in spacy_nlp(sentence):
                word = token.lemma_
                tempSent = tempSent + ' ' + word
            sentence = tempSent
            word_count_in_sentence = len(word_tokenize(sentence))
            for wordValue in freqTable:
                if wordValue.lower() in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freqTable[wordValue]
                    else:
                        sentenceValue[sentence] = freqTable[wordValue]
            #commonLog.log(sentence)
            try:
                #commonLog.log(f'------->>>>>{sentence}------>>>')
                sentenceValue[sentence] = sentenceValue[sentence] // word_count_in_sentence
            except KeyError:
                pass
        return sentenceValue

    @staticmethod
    def findAverageScore(sentenceValue):
        """ Finding average score of a sentence from a text corpus """
        sumValues = 0
        for entry in sentenceValue:
            sumValues += sentenceValue[entry]
        average = int(sumValues/len(sentenceValue))
        return average

    @staticmethod
    def generateSummaryBasedOnSentenceScore(sentenceValue, threshold, numberOfSentences=10):
        """  Generating Summary with the sentences which are having above average sentence score """
        list1 = sorted(sentenceValue.items(), key=operator.itemgetter(1), reverse=True)
        sentences = []
        for sent in list1:
            sentences.append(sent[0])
        sentence_count = 0
        summary = ''
        for sentence in sentences:
            tempSent = ''
            if sentence in sentenceValue and sentenceValue[sentence] > threshold and numberOfSentences > 0:
                numberOfSentences = numberOfSentences - 1
                summary += " " + sentence
                sentence_count += 1
        return summary
