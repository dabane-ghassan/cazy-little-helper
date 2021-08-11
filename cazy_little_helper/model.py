#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
the ML Model class, a TF-IDF/SVM classifier. The class will scrape the articles
(only PMC full articles) and preprocess them before vectorizing with TF-IDF.

@author: dabane-ghassan
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
from cazy_little_helper.preprocessor import Preprocessor
from cazy_little_helper.scraper import Scraper

class Model:
    """A class to represent the architecture of CAZy's little helper,
    A TF-IDF/SVM classifier.

    Attributes
    ----------
    path : str
        The output save path of the model.

    dataset : pandas.DataFrame
        The dataset to scrape and train, a two column .csv file, "id" column
        with a list of PMCIDs, and a "label" column indicating the
        compatibility of an article with the database, annotated by
        researchers.
    
    val_size : float
        The validation dataset size.
    
    architecture: sklearn.pipeline.Pipeline
        The scikit learn pipeline representing the architecture.
    
    scraper: cazy_little_helper.scraper.Scraper
        A scraper object to collect the full text PMC articles.
    
    processor: cazy_little_helper.preprocessor.Preprocessor
        A preprocessor object to clean and tokenize documents.
        
    X_train: List[str]
        The training dataset.

    y_train: List[int]
        The training labels.
        
    X_val: List[str]
        The validation dataset.

    y_val: List[int]
        The validation labels.

    """
    def __init__(
        self: object,
        path: str,
        dataset: str,
        biblio_address: str,
        val_size: float
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        path : str
            The output save path of the model.
        dataset : str
            The path of the training dataset.
        biblio_address : str
            The path of the biblio package.
        val_size : float
            Validation dataset size.

        Returns
        -------
        None
            Class instance.

        """
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
        """X_train property getter.

        Returns
        -------
        List[str]
            The training set.

        """
        return self.__X_train

    @X_train.setter
    def X_train(
        self: object,
        param_x_train: List[str]
    ) -> None:
        """X_train property setter.

        Parameters
        ----------
        param_x_train : List[str]
            The new value.

        Returns
        -------
        None
            Sets a new value for the property.

        """
        self.__X_train = param_x_train

    @property
    def y_train(
        self: object
    ) -> List[int]:
        """y_train property getter.

        Returns
        -------
        List[str]
            The training labels.

        """
        return self.__y_train

    @y_train.setter
    def y_train(
        self: object,
        param_y_train: List[int]
    ) -> None:
        """y_train property setter.

        Parameters
        ----------
        param_y_train : List[str]
            The new value.

        Returns
        -------
        None
            Sets a new value for the property.

        """
        self.__y_train = param_y_train

    @property
    def X_val(
        self: object
    ) -> List[str]:
        """X_val property getter.

        Returns
        -------
        List[str]
            The validation set.

        """
        return self.__X_val

    @X_val.setter
    def X_val(
        self: object,
        param_x_val: List[str]
    ) -> None:
        """X_val property setter.

        Parameters
        ----------
        param_x_val : List[str]
            The new value.

        Returns
        -------
        None
            Sets a new value for the property.

        """
        self.__X_val = param_x_val

    @property
    def y_val(
        self: object
    ) -> List[int]:
        """y_val property getter.

        Returns
        -------
        List[str]
            The validation labels.

        """
        return self.__y_val
    
    @y_val.setter
    def y_val(
        self: object,
        param_y_val: List[int]
    ) -> None:
        """y_val property setter.

        Parameters
        ----------
        param_y_val : List[str]
            The new value.

        Returns
        -------
        None
            Sets a new value for the property.

        """
        self.__y_val = param_y_val

    def dataset_prep(
        self: object
    ) -> None:
        """This method prepares the dataset for training, first start by
        scraping articles using the bilbio tool, then process to parse them
        and preprocess them for training (including tokenization), then lastly
        finish by splitting it into a training and validation datasets.

        Returns
        -------
        None
            Sets the training and validation object properties.

        """
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
        """This method fits the architecture with the training dataset.

        Returns
        -------
        None
            Fits the architecture property.

        """
        self.architecture.fit(self.X_train, self.y_train)

    def performance(
        self: object
    ) -> None:
        """This method makes predictions on the validation dataset and prints
        out some classification statistics

        Returns
        -------
        None
            Prints accuracy stats on the validation dataset.

        """
        print(classification_report(self.y_val,
                                    self.architecture.predict(self.X_val)))

    def save(
        self: object
    ) -> None:
        """Saves the model to the specified path with joblib.

        Returns
        -------
        None
            Prints the save path of the model.

        """
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
        """A class method to construct a model and train it with a one-liner.

        Parameters
        ----------
        cls : object
            A Model class instance.
        path : str
            The output save path of the model.
        dataset : str
            The path of the training dataset.
        biblio_address : str
            The path of the biblio package.
        val_size : float
            Validation dataset size.

        Returns
        -------
        object
            A class instance.

        """
        model = cls(path, dataset, biblio_address, val_size)
        model.dataset_prep()
        model.fit()
        model.performance()
        model.save()
        return model
