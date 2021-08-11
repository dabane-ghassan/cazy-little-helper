#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A CLI entry point for the PyPI package, for making predictions with CAZy's 
little helper.

@author: dabane-ghassan
"""
from __future__ import absolute_import
from parsers import Parser
from pipeline import Pipeline

def launch_pipeline( 
    input_data: str,
    id_pos: int,
    biblio_address: str,
    model: str,
) -> None:

    process = Pipeline(input_data, id_pos, biblio_address, model)
    process.run()

def main(
) -> None:

    parser = Parser.predict()
    args = parser.parse_args()
    args = args.__dict__
    launch_pipeline(args["input_path"], args["id_pos"],
                    args["biblio_add"], args["model"])

if __name__ == "__main__":
    main()
