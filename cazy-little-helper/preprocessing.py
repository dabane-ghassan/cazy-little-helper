#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 14:29:16 2021

@author: ghassandabane
"""
import gensim
import re
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer, PorterStemmer
from typing import List, Generator

def clean_doc(
        doc: str
) -> str:

    doc = str(doc).lower()
    doc = doc.replace('{html}', "")
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', doc)
    rem_url = re.sub(r'http\S+', '', cleantext)
    rem_www = re.sub(r'www\S+', '', rem_url)
    rem_entrez = re.sub(r'\{([^)]+)\}', '', rem_www)
    rem_num = re.sub(r'^\d+(?:,\d*)?$', '', rem_entrez)
    return rem_num

def preprocess(
        texts: List[str]
) -> Generator[List[str], None, None] :

    for doc in texts:
        cleaned_doc = clean_doc(doc)
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(cleaned_doc)
        yield tokens

def remove_stopwords(
        texts: List[List[str]]
) -> List[List[str]]:

    stop_words = stopwords.words('english')
    stop_words.extend(
        ['from', 'subject', 're', 'edu', 'use', 'however',
         'et', 'al', 'fig', 'also', 'conflict', 'interest']
        )

    return [[
        w for w in doc if len(w) > 3 if w not in stop_words
        if not w.isnumeric()
    ] for doc in texts]

def make_ngrams(
        texts: List[List[str]]
) -> List[List[str]]:

    bigram = gensim.models.Phrases(
        texts, min_count=5,
        threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram = gensim.models.Phrases(bigram[texts], threshold=100)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def stemmer(
        texts: List[List[str]]
) -> List[List[str]]:

    stemmer = PorterStemmer()
    return [[stemmer.stem(w) for w in doc] for doc in texts]

def lemmatizer(
        texts: List[List[str]]
) -> List[List[str]]:

    lemmatizer = WordNetLemmatizer()
    return [[lemmatizer.lemmatize(w) for w in doc] for doc in texts]

def preprocess_pipeline(
        docs: List[str]
) -> List[List[str]]:

    data_words_raw = list(preprocess(docs))
    data_words_no_stop = remove_stopwords(data_words_raw)
    data_words_ngrams = make_ngrams(data_words_no_stop)
    data_words_stemmed = stemmer(data_words_ngrams)
    data_words = lemmatizer(data_words_stemmed)

    return data_words
