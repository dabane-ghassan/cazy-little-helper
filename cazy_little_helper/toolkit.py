#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Some tools to clean and scrape the dataset.

@author: Ghassan
"""
from __future__ import absolute_import
import os
import pandas as pd
from metapub.pubmedcentral import get_pmid_for_otherid
from metapub.pubmedcentral import get_pmcid_for_otherid
from metapub.pubmedcentral import get_doi_for_otherid

class Toolkit:

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
