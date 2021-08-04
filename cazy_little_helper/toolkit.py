#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Some tools to clean and scrape the dataset.

@author: Ghassan
"""

class Toolkit:

    @staticmethod
    def is_doi(expr: str) -> bool:
        """Verifies if a given expression is a DOI link.
    
        Parameters
        ----------
        expr : str
            The expression to be verified.
    
        Returns
        -------
        bool
    
        """
        return ("/" in expr)

    @staticmethod
    def is_pmc(expr: str) -> bool:
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
    def not_found(expr: str) -> bool:
        """Verifies if a given expression is not found when trying to find a PMID
        from a DOI or when trying to find a PMCID from a PMID.
    
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
    def all_doi_to_pmid(file_name: str) -> str:
        """This function transforms all DOI links in a file to PMID if available,
        when not available, it will leave the DOI links as they are.
    
        Parameters
        ----------
        file_name : str
            The file path.
    
        Returns
        -------
        str
            The new file path.
    
        """
        pass

    @staticmethod
    def all_pmid_to_pmcid(pmid_file: str) -> str:
        """This function transforms all PMIDs in a file to PMCIDs if available,
        when not available, it will leave the PMIDs as they are.
    
        Parameters
        ----------
        file_name : str
            The file path.
    
        Returns
        -------
        str
            The new file path.
    
        """
        pass
