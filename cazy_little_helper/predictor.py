#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 10:38:26 2021

@author: ghassan
"""
from joblib import load
from typing import Optional, List

class Scorer:

    def __init__(
        self: object,
        docs: List[str], 
        model: Optional[str]="../model/cazy_helper.joblib",
    ) -> None:

        self.model = load(model)
        self.docs = docs
        
    def confidence(
        self: object
    ) -> List[float]:

        return self.model.predict_proba(self.docs)[:, 1] * 100
