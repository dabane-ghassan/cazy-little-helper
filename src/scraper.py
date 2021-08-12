#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A scraper class.

@author: dabane-ghassan
"""
from __future__ import absolute_import
from typing import List
import os
import time
import csv
import requests
from bs4 import BeautifulSoup
from metapub import PubMedFetcher

class Scraper:
    """A scraper class that uses the Biblio package to scrape articles,
    when PMCID is not available, scrapes the abstracts with metapub.

    Attributes
    ----------
    text_dataset: str
        The path of scraped articles dataset.

    biblio_adress: str
        The Bilbio package address on the server.

    """
    def __init__(
        self: object,
        input_data: str,
        biblio_address: str
    ) -> None:
        """Class constructor

        Parameters
        ----------
        input_data : str
            The input data path.
        biblio_address : str
            The biblio package web address.

        Returns
        -------
        None
            Class instance.

        """
        self.text_dataset = "%s_text.csv" %(os.path.splitext(input_data)[0])
        self.biblio_address = biblio_address

    def scrape_biblio(
        self: object,
        pmcids: List[str]
    ) -> None:
        """This method uses the Biblio package to scrape full PMC articles.

        Parameters
        ----------
        pmcids : List[str]
            A list of PMCIDs to scrape.

        Returns
        -------
        None
            Scrapes PMC articles and writes them out to a .csv file.

        """
        biblio = self.biblio_address + \
            "/utils/fromPMCID/fromPMCID.php?PMCID=%s&print&content&title"

        with open(self.text_dataset, "w") as new_file:

            writer = csv.writer(new_file)
            writer.writerow(["id", "title", "only_abstract", "text"])
            for pmcid in pmcids:
                pmcidi = pmcid[3:].strip()
                try:
                    url = biblio%(pmcidi)
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

    def fetch_abstracts(
        self: object,
        pmids: List[str]
    ) -> None:
        """This method is used to fetch abstracts for articles without a PMCID.
        Runs after the last method.

        Parameters
        ----------
        pmids : List[str]
            A list of article PMIDs.

        Returns
        -------
        None
            Fetches abstracts using PMIDs after the Biblio scraping is
            finished.

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
