#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A Preprocessor class.

@author: dabane-ghassan
"""
from __future__ import absolute_import
import re
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer, PorterStemmer
from typing import List, Generator, Optional

class Preprocessor:
    """A preprocessing class to clean documents, tokenize, and create bi-gram
    and tri-gram model.

    Attributes
    ----------
    docs: Optional[List[str]]
        The documents to be processed, a list of strings.

    """
    def __init__(
        self: object,
        docs: Optional[List[str]]=None
    ) -> None:
        """Class constructor

        Parameters
        ----------
        docs : Optional[List[str]], optional
            The documents to be processed. The default is None.

        Returns
        -------
        None
            A class instance.

        """
        self.docs = docs

    @staticmethod
    def clean_doc(
        doc: str
    ) -> str:
        """This function cleans a given document to reduce the noise.

        Parameters
        ----------
        doc : str
            The document to be cleaned, a string.

        Returns
        -------
        str
            The cleaned document.

        """
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
        """This function tokenizes a corpus of texts.

        Parameters
        ----------
        texts : List[str]
            The documents to be tokenized.

        Yields
        ------
        Generator[List[str], None, None]
            A list of tokenzied documents.

        """
        for doc in texts:
            cleaned_doc = Preprocessor.clean_doc(doc)
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(cleaned_doc)
            yield tokens

    @staticmethod
    def remove_stopwords(
        texts: List[List[str]]
    ) -> List[List[str]]:
        """Removes stopwords inside a corpus of documents.

        Parameters
        ----------
        texts : List[List[str]]
            The documents to be cleaned.

        Returns
        -------
        List[List[str]]
            The cleaned documents.

        """
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
        """Creates n-grams (bi- and tri-) from a corpus of documents.

        Parameters
        ----------
        texts : List[List[str]]
            The corpus of documents.

        Returns
        -------
        List[List[str]]
            The corpus with bi- and tri-grams.   

        """
        bigram = Phrases(texts, min_count=5, threshold=100)
        bigram_mod = Phraser(bigram)
        trigram = Phrases(bigram[texts], threshold=100)
        trigram_mod = Phraser(trigram)
        return [trigram_mod[bigram_mod[doc]] for doc in texts]

    @staticmethod
    def stemmer(
        texts: List[List[str]]
    ) -> List[List[str]]:
        """This functions stems words inside a corpus.

        Parameters
        ----------
        texts : List[List[str]]
            The corpus of documents.

        Returns
        -------
        List[List[str]]
            The stemmed corpus.

        """
        stemmer = PorterStemmer()
        return [[stemmer.stem(w) for w in doc] for doc in texts]

    @staticmethod
    def lemmatizer(
        texts: List[List[str]]
    ) -> List[List[str]]:
        """This function lemmatizes a corpus.

        Parameters
        ----------
        texts : List[List[str]]
            The corpus of documents.

        Returns
        -------
        List[List[str]]
            The lemmatized corpus.

        """
        lemmatizer = WordNetLemmatizer()
        return [[lemmatizer.lemmatize(w) for w in doc] for doc in texts]

    @staticmethod
    def preprocess(
        docs: List[str]
    ) -> List[List[str]]:
        """This function is used to run the whole preprocessing on a corpus.
        very easy to use outside the pipeline.

        Parameters
        ----------
        docs : List[str]
            A corpus of unprocessed documents.

        Returns
        -------
        List[List[str]]
            The preprocessed corpus.

        """
        data_words_raw = list(Preprocessor.tokenize(docs))
        data_words_no_stop = Preprocessor.remove_stopwords(data_words_raw)
        data_words_ngrams = Preprocessor.make_ngrams(data_words_no_stop)
        data_words_stemmed = Preprocessor.stemmer(data_words_ngrams)
        data_words = Preprocessor.lemmatizer(data_words_stemmed)
        return data_words

    def pipeline(
        self: object
    ) -> List[List[str]]:
        """Thie class method is used to run the preprocessing pipeline on the 
        object, intended as a one-liner for the Pipeline class.

        Returns
        -------
        List[List[str]]
            The preprocessed corpus of documents.

        """
        return Preprocessor.preprocess(self.docs)
