#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 14:11:53 2021

@author: ghassandabane
"""
from __future__ import absolute_import
from parsers import Parser
from model import Model

def launch_create_model( 
    path: str,
    dataset: str,
    biblio_address: str,
    val_size: float
) -> Model:

    return Model.create_model(path, dataset, biblio_address, val_size)

def main(
) -> None:

    parser = Parser.create_model()
    args = parser.parse_args()
    args = args.__dict__
    launch_create_model(args["output_path"], args["dataset"],
                                 args["biblio_add"], args["val_size"])

if __name__ == "__main__":
    main()