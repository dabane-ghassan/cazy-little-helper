#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 10:50:22 2021

@author: ghassan
"""
import os
import time
import csv
import requests
from bs4 import BeautifulSoup
from metapub import PubMedFetcher
from typing import List

class Scraper:

    def __init__(
        self: object,
        ids_dataset: List[str],
        biblio_address: str
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        ids : List[str]
            DESCRIPTION.
        biblio_address : str
            DESCRIPTION.

        Returns
        -------
        None
            DESCRIPTION.

        """
        self.text_dataset = "%s_text.csv" %(os.path.splitext(ids_dataset)[0])
        self.bibio_address = biblio_address

    def scrape(
        self: object,
        pmcids: List[str]
    ) -> None:
        """A Method to scrape full articles with PMCIDs using the biblio 
        package.
    
        Parameters
        ----------
        pmcids : List[str]
            The list of PMCIDs.

        Returns
        -------
        None
            Scrapes full-text PMC article to the text_dataset.
        """
        biblio = self.biblio_address + \
            "/utils/fromPMCID/fromPMCID.php?PMCID=%s&print&content&title"

        with open(self.text_dataset, "w") as new_file:

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

    def fetch_abstracts(
        self: object,
        pmids: List[str]
    ) -> None:
        """A method to fetch abstracts from a list of PMIDs after the 
        scraping function has finished. Predictions based on abstracts will 
        be less fiable but better than nothing at all.
    
        Parameters
        ----------
        pmids : List[str]
            The list of PMIDs to scrape, PMIDs with no associated PMCIDs.
    
        Returns
        -------
        None
            Fetches abstracts to the text dataset after the scrape method.
        """
        fetcher = PubMedFetcher()    
        with open(self.text_dataset, "a") as f:
            writer = csv.writer(f)
            for pmid in pmids:
                only_abstract = True
                text = fetcher.article_by_pmid(pmid).abstract
                title = fetcher.article_by_pmid(pmid).title
                writer.writerow([pmid, title, only_abstract, text])
                time.sleep(3)
