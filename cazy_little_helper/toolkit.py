#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Some tools to clean and scrape the dataset.

@author: Ghassan
"""
import csv
import time
import requests
from bs4 import BeautifulSoup
from typing import List
from metapub import PubMedFetcher

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

    @staticmethod        
    def scrape(output: str, pmcids: List[str]) -> str:
        """A function to scrape full articles with PMCIDs.
    
        Parameters
        ----------
        output : str
            The output dataset file path.
        pmcids : List[str]
            The list of PMCIDs.
    
        Returns
        -------
        str
            The output dataset file path.
        """
        ### Biblio package
        biblio = "http://localhost/Biblio/utils/fromPMCID/fromPMCID.php?PMCID=%s&print&content&title"
    
        with open(output, "w") as new_file:
    
            writer = csv.writer(new_file)
            writer.writerow(["id", "title", "only_abstract", "text"])
            for pmcid in pmcids:
                pmcidi = pmcid[3:].strip() #taking out the "PMC" from the beginning
                try:
                    url = biblio%(pmcidi) #using the biblio package
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.find_all('h1')[0].text
                    text = ''.join([p.text for p in soup.find_all('p')])
                    only_abstract = True
                    if len(soup.find_all('h2')) > 1:
                        only_abstract = False
                    writer.writerow([pmcid, title, only_abstract, text])
                    time.sleep(3)
    
                except IndexError:
                    print("problem with article PMC%s"%(pmcidi))
                    pass
        return output
    
    @staticmethod
    def fetch_abstracts(text_docs: str, pmids: List[str]) -> str:
        """A function to fetch abstracts from a list of PMIDs after the scraping
        function has finished.
    
        Parameters
        ----------
        text_docs : str
            The scraped PMCIDs dataset file path.
        pmids : List[str]
            The list of PMIDs to scrape, PMIDs with no associated PMCIDs.
    
        Returns
        -------
        str
            The dataset file path.
        """
        fetch = PubMedFetcher()    
        with open(text_docs, "a") as f:
            writer = csv.writer(f)
            for pmid in pmids:
                only_abstract = True
                text = fetch.article_by_pmid(pmid).abstract
                title = fetch.article_by_pmid(pmid).title
                writer.writerow([pmid, title, only_abstract, text])
                time.sleep(3)
    
        return text_docs
