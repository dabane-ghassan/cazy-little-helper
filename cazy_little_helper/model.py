#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 10:39:48 2021

@author: ghassan
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from preprocessor import preprocess_pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
#from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.calibration import CalibratedClassifierCV
from joblib import load

class Model:
    pass