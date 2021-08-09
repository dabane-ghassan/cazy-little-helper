#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 10:57:03 2021

@author: ghassandabane
"""
from __future__ import absolute_import
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

class Parser:

    @staticmethod
    def predict(
    ) -> ArgumentParser:

        describe= "Welcome to CAZy's little helper ▼(´ᴥ`)▼ !\n\
    The biocuration assistant of the CAZy database, woof woof.\n\
    CAZy's little helper takes a .csv file that contains a list of PMIDS and \
    spits out another file with a confidence score for the given articles.\n\
    Please visit https://github.com/dabane-ghassan/cazy-little-helper \
    for more information about the package."
    
        parser = ArgumentParser(add_help=True,
                                         description=describe,
                                         formatter_class=RawTextHelpFormatter)
    
        parser.add_argument('-i','--input_path',
                            type=str,
                            required=True,
                            default=sys.stdin,
                            help="[REQUIRED] The input data file path,\
    a .csv file with a column of article IDs")

        parser.add_argument('-p','--id_pos',
                            type=int,
                            required=False,
                            default=0,
                            help="[OPTIONAL] The index of the ID column in the \
    input file path, default is 0 (first column).")

        parser.add_argument('-b','--biblio_add',
                            type=str,
                            required=False,
                            default="http://localhost/Biblio",
                            help="[OPTIONAL] The address of the biblio package \
    on the php server, default is http://localhost/Biblio")

        parser.add_argument('-m','--model',
                                type=str,
                                required=False,
                                default="../model/cazy_helper.joblib",
                                help="[OPTIONAL] The model path to run the \
    predictions, default is the CAZy's little helper already trained model \
    based on Aug 2021 data, '../model/cazy_helper.joblib'")

        return parser

    @staticmethod
    def find_ids(
    ) -> ArgumentParser:

        describe= "Welcome to CAZy's little helper ▼(´ᴥ`)▼ !\n\
    The biocuration assistant of the CAZy database, woof woof.\n\
    This special functionality takes a list of articles IDs and tries to find \
    another corresponding type of ID. Works best if we have a list of mixed \
    IDs and we want to find the corresponding PMIDs in order to run the main \
    CAZy's little helper prediction pipeline, but can be used to find any other \
    type of ids.\n\
    Please visit https://github.com/dabane-ghassan/cazy-little-helper \
    for more information about the package."

        parser = ArgumentParser(add_help=True,
                                         description=describe,
                                         formatter_class=RawTextHelpFormatter)

        parser.add_argument('-i','--input_path',
                            type=str,
                            required=True,
                            default=sys.stdin,
                            help="[REQUIRED] The input ID file path, \
    a .csv file with a column of article IDs")

        parser.add_argument('-t','--id_type',
                            type=str,
                            required=False,
                            default=sys.stdin,
                            help="[REQUIRED] The type of ID to find, \
    ['PMID', 'PMCID', 'DOI'], uppercase only")

        return parser
