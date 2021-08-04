#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 14:29:16 2021

@author: ghassandabane
"""
import re
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer, PorterStemmer
from typing import List, Generator

class Preprocessor:

    def __init__(
        self: object,
        docs: List[str]
    ) -> None:

        self.docs = docs

    @staticmethod
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

    @staticmethod
    def tokenize(
        texts: List[str]
    ) -> Generator[List[str], None, None]:

        for doc in texts:
            cleaned_doc = Preprocessor.clean_doc(doc)
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(cleaned_doc)
            yield tokens

    @staticmethod
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

    @staticmethod
    def make_ngrams(
        texts: List[List[str]]
    ) -> List[List[str]]:

        bigram = Phrases(texts, min_count=5, threshold=100)
        bigram_mod = Phraser(bigram)
        trigram = Phrases(bigram[texts], threshold=100)
        trigram_mod = Phraser(trigram)
        return [trigram_mod[bigram_mod[doc]] for doc in texts]

    @staticmethod
    def stemmer(
        texts: List[List[str]]
    ) -> List[List[str]]:

        stemmer = PorterStemmer()
        return [[stemmer.stem(w) for w in doc] for doc in texts]

    @staticmethod
    def lemmatizer(
        texts: List[List[str]]
    ) -> List[List[str]]:

        lemmatizer = WordNetLemmatizer()
        return [[lemmatizer.lemmatize(w) for w in doc] for doc in texts]

    @staticmethod
    def preprocess(
        docs: List[str]
    ) -> List[List[str]]:

        data_words_raw = list(Preprocessor.tokenize(docs))
        data_words_no_stop = Preprocessor.remove_stopwords(data_words_raw)
        data_words_ngrams = Preprocessor.make_ngrams(data_words_no_stop)
        data_words_stemmed = Preprocessor.stemmer(data_words_ngrams)
        data_words = Preprocessor.lemmatizer(data_words_stemmed)
        return data_words

    def pipeline(
        self: object
    ) -> List[List[str]]:

        return Preprocessor.preprocess(self.docs)
