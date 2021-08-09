#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 15:44:01 2021

@author: ghassandabane
"""
from __future__ import absolute_import
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from pipeline import Pipeline

def launch_pipeline( 
    input_data: str,
    id_pos: int,
    biblio_address: str
) -> None:

    process = Pipeline(input_data, id_pos, biblio_address)
    process.run()

def create_parser(
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

    return parser

def main(
) -> None:

    parser = create_parser()
    args = parser.parse_args()
    args = args.__dict__
    launch_pipeline(args["input_path"], args["id_pos"], args["biblio_add"])

if __name__ == "__main__":
    main()
