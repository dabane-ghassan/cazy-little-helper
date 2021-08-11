#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A CLI entry point for the PyPI package, for launching find_ids functionality.

@author: dabane-ghassan
"""
from __future__ import absolute_import
from cazy_little_helper.parsers import Parser
from cazy_little_helper.toolkit import Toolkit

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
