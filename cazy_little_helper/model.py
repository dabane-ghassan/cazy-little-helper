#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 10:39:48 2021

@author: ghassan
"""
from __future__ import absolute_import
from typing import List
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.calibration import CalibratedClassifierCV
from sklearn.utils import shuffle
from joblib import dump
from preprocessor import Preprocessor
from scraper import Scraper

class Model:

    def __init__(
        self: object,
        path: str,
        dataset: str,
        biblio_address: str,
        val_size: float
    ) -> None:

        self.path = path
        self.dataset = shuffle(pd.read_csv(dataset))
        self.val_size = val_size
        self.architecture = Pipeline([
            ("tfidf_vectorization", TfidfVectorizer()),
            ("classifier", CalibratedClassifierCV(LinearSVC(C=10)))
            ])
        self.scraper = Scraper(dataset, biblio_address)
        self.processor = Preprocessor()
        self.__X_train, self.__y_train = None, None
        self.__X_val, self.__y_val = None, None

    @property
    def X_train(
        self: object
    ) -> List[str]:

        return self.__X_train
    
    @X_train.setter
    def X_train(
        self: object,
        param_x_train: List[str]
    ) -> None:

        self.__X_train = param_x_train
        
    @property
    def y_train(
        self: object
    ) -> List[int]:

        return self.__y_train
    
    @y_train.setter
    def y_train(
        self: object,
        param_y_train: List[int]
    ) -> None:

        self.__y_train = param_y_train
        
    @property
    def X_val(
        self: object
    ) -> List[str]:

        return self.__X_val
    
    @X_val.setter
    def X_val(
        self: object,
        param_x_val: List[str]
    ) -> None:

        self.__X_val = param_x_val

    @property
    def y_val(
        self: object
    ) -> List[int]:

        return self.__y_val
    
    @y_val.setter
    def y_val(
        self: object,
        param_y_val: List[int]
    ) -> None:

        self.__y_val = param_y_val

    def dataset_prep(
        self: object
    ) -> None:

        print("Scraping articles...")
        self.scraper.scrape_biblio(self.dataset.id.to_list())

        print("Parsing scraped documents and preparing the dataset...")
        df_data_text = pd.read_csv(self.scraper.text_dataset)
        df_data_text  = df_data_text.fillna('')
        df_data_text["docs"] = df_data_text["title"] + " " + \
            df_data_text["text"]
        df_data_text.drop(['title','text','only_abstract'],
                          inplace=True, axis=1)
        self.dataset = pd.merge(self.dataset, df_data_text, on='id')

        print("Preprocessing documents for training...")
        self.processor.docs = self.dataset.docs.to_list()
        data_words = self.processor.pipeline()

        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
           np.array([" ".join(doc) for doc in data_words]),
           self.dataset.label.values,
           test_size=self.val_size)

    def fit(
        self: object
    ) -> None:

        self.architecture.fit(self.X_train, self.y_train)

    def performance(
        self: object
    ) -> None:

        print(classification_report(self.y_val,
                                    self.architecture.predict(self.X_val)))

    def save(
        self: object
    ) -> None:

        print("The model was saved to %s" % (dump(self.architecture,
                                                  self.path)[0]))

    @classmethod
    def create_model(
        cls: object,
        path: str,
        dataset: str,
        biblio_address: str  ,
        val_size: float
    ) -> object:

        model = cls(path, dataset, biblio_address, val_size)
        model.dataset_prep()
        model.fit()
        model.performance()
        model.save()
        return model
