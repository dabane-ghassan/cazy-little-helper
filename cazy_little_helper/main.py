#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 15:44:01 2021

@author: ghassandabane
"""
from __future__ import absolute_import
import argparse
import sys
from pipeline import Pipeline

def launch_pipeline( 
    input_data: str,
    id_pos: int,
    biblio_address: str
) -> None:

    process = Pipeline(input_data, id_pos, biblio_address)
    process.run()

def create_parser(
) -> argparse.ArgumentParser:
    
    describe= "Welcome to CAZy's little helper ▼(´ᴥ`)▼! \n \
        the biocuration assistant of the CAZy database, woof woof."

    parser = argparse.ArgumentParser(add_help=True,
                                     description=describe)
    
    parser.add_argument('-i','--input_path',
                        type=str,
                        required=True,
                        default=sys.stdin,
                        help="[REQUIRED] The input data file path, \
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
                            on the php server, default is \
                                http://localhost/Biblio")

    return parser

def main(
) -> None:
    """This function instantiates an argument parser object and calls
    selec_seqs_list function to return sequences for user specified IDs
    from the given fasta file.
    """
    parser = create_parser()
    args = parser.parse_args()
    args = args.__dict__
    launch_pipeline(args["input_path"], args["id_pos"], args["biblio_add"])

if __name__ == "__main__":
    main()
