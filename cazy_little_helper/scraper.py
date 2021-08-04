#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 10:50:22 2021

@author: ghassan
"""
import time
import csv
import requests
from bs4 import BeautifulSoup
from metapub import PubMedFetcher
from typing import List

class Scraper:

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
