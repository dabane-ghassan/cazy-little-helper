#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 15:44:01 2021

@author: ghassandabane
"""
from __future__ import absolute_import
from parsers import Parser
from pipeline import Pipeline

def launch_pipeline( 
    input_data: str,
    id_pos: int,
    biblio_address: str
) -> None:

    process = Pipeline(input_data, id_pos, biblio_address)
    process.run()

def main(
) -> None:

    parser = Parser.predict()
    args = parser.parse_args()
    args = args.__dict__
    launch_pipeline(args["input_path"], args["id_pos"], args["biblio_add"])

if __name__ == "__main__":
    main()
