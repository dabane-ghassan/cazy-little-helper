#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 10:29:26 2021

@author: ghassandabane
"""
from __future__ import absolute_import
from parsers import Parser
from toolkit import Toolkit

def launch_find( 
    ids_file: str,
    id_type: str
) -> None:

    return Toolkit.find_ids(ids_file, id_type)

def main(
) -> None:

    parser = Parser.find_ids()
    args = parser.parse_args()
    args = args.__dict__
    output = launch_find(args["input_path"], args["id_type"])
    print("the file was saved to %s"%(output))

if __name__ == "__main__":
    main()
