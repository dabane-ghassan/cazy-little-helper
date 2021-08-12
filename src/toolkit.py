#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A Toolkit class.

@author: dabane-ghassan
"""
from __future__ import absolute_import
import os
import pandas as pd
from metapub.pubmedcentral import get_pmid_for_otherid
from metapub.pubmedcentral import get_pmcid_for_otherid
from metapub.pubmedcentral import get_doi_for_otherid

class Toolkit:
    """A Toolkit class to wrap some useful functions.

    Attributes
    ----------
    None

    """
    @staticmethod
    def is_doi(
        expr: str
    ) -> bool:
        """Verifies if a given expression is a DOI link.

        Parameters
        ----------
        expr : str
            The expression to be verified.

        Returns
        -------
        bool

        """
        return "/" in expr

    @staticmethod
    def is_pmc(
        expr: str
    ) -> bool:
        """Verifies if a given expression is a PMCID.

        Parameters
        ----------
        expr : str
            The expression to be verified.

        Returns
        -------
        bool

        """
        return expr.startswith("PMC")

    @staticmethod
    def not_found(
        expr: str
    ) -> bool:
        """Verifies if a given expression is not found when trying to find
        a PMID from a DOI or when trying to find a PMCID from a PMID.

        Parameters
        ----------
        expr : str
            The expression to be verified.

        Returns
        -------
        bool

        """
        return expr.startswith("N")

    @staticmethod
    def find_ids(
        ids_file: str,
        id_type: str
    ) -> str:
        """This function transforms a list of articles IDs into another type. 

        Parameters
        ----------
        ids_file : str
            The IDs list, a .csv file with only one column wihtout a header.
        id_type : str
            The type of ID to search for, one of the following,
            ['PMID', 'DOI', 'PMCID'].

        Raises
        ------
        Exception
            Stop the process when the specified ID type is not allowed.

        Returns
        -------
        str
            The output file path.

        """
        if id_type == "PMID":
            finder = get_pmid_for_otherid
        elif id_type == "DOI":
            finder = get_doi_for_otherid
        elif id_type == "PMCID":
            finder = get_pmcid_for_otherid
        else:
            raise Exception("ID type error, please provide one of the \
                            following three = ['PMID', 'DOI', 'PMCID']")

        ids = pd.read_csv(ids_file, header=None)[0]
        output = "%s_%s.csv" % (os.path.splitext(ids_file)[0], id_type)
        pmids = []

        for idi in ids:
            try:
                if pmid := finder(idi):
                    pmids.append(pmid)
                else:
                    pmids.append("not_found")
            except AttributeError:
                pmids.append("not_found")

        pd.DataFrame({"id": ids,
                      id_type: pd.Series(pmids)
                    }).to_csv(output, index=False)

        return output
