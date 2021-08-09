#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 10:29:26 2021

@author: ghassandabane
"""

from __future__ import absolute_import
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from toolkit import Toolkit

def launch_find( 
    ids_file: str,
    id_type: str
) -> None:

    return Toolkit.find_ids(ids_file, id_type)

def create_parser(
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

def main(
) -> None:

    parser = create_parser()
    args = parser.parse_args()
    args = args.__dict__
    output = launch_find(args["input_path"], args["id_type"])
    print("the file was saved to %s"%(output))

if __name__ == "__main__":
    main()
