#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A Scorer class to make prediction inside an analysis pipeline.

@author: ghassan
"""
from __future__ import absolute_import
from typing import Optional, List
from joblib import load

class Scorer:
    """A Scorer class to give a confidence score on new articles, based on
    a given model.

    Attributes
    ----------
    model: sklearn.pipeline.Pipeline
        CAZy's little helper model - a TF-IDF/SVM architecture.

    docs: Optional[List[str]]
        The documents to make predictions on, a list of strings.

    """
    def __init__(
        self: object,
        model: str,
        docs: Optional[List[str]]=None
    ) -> None:
        """The class constructor.

        Parameters
        ----------
        model : str
            The model path to load using joblib.
    
        docs : Optional[List[str]], optional
            The preprocessed corpus of documents. The default is None.

        Returns
        -------
        None
            A class instance.

        """
        self.model = load(model)
        self.docs = docs

    def confidence(
        self: object
    ) -> List[float]:
        """

        Returns
        -------
        List[float]
            A list of floats .

        """
        

        return self.model.predict_proba(self.docs)[:, 1] * 100
