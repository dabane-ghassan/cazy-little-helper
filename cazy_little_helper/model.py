#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 10:39:48 2021

@author: ghassan
"""
from __future__ import absolute_import
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.calibration import CalibratedClassifierCV
from joblib import dump
from preprocessor import Preprocessor

class Model:

    def __init__(
        self: object,
        path: str,
        dataset: str
    ) -> None:

        self.path = path
        self.dataset = pd.read_csv(dataset)
        self.architecture = Pipeline([
            ("tfidf_vectorization", TfidfVectorizer()),
            ("classifier", CalibratedClassifierCV(LinearSVC(C=10)))
            ])

    def dataset_prep(
        self: object,
        test_size: float
    ) -> None:

        processor = Preprocessor()
        processor.docs = df_data_text.docs.to_list()
        df_data_words = processor.pipeline()

        print("Predicting confidence score...")
        df["processed_docs"] = np.array([" ".join(doc) for doc in df_data_words])
        
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
           df.processed_docs.values, df.label.values, test_size=0.15)

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
    ) -> str:
        return dump(self.architecture, self.path)[0]
