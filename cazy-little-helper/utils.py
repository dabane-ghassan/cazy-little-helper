#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Some tools to clean and scrape the dataset.

@author: Ghassan
"""
import os
import csv
import time
import requests
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from typing import List
from metapub import PubMedFetcher

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
    name, ext = os.path.splitext(file_name)
    new_file = "%s_all_pmid%s" % (name, ext)

    with open(file_name, "r") as file_handler, open(new_file,
                                                    "w") as file_writer:
        for line in file_handler:
            if is_doi(line):
                output = os.popen('php search_pmid_if_doi.php "%s"' %(
                    line)).read()
                if not_found(output):
                    file_writer.write(line)
                else:
                    file_writer.write(output)
            else:
                file_writer.write(line)
    return new_file

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
    name, ext = os.path.splitext(pmid_file)
    new_file = "%s_pmcid%s" % (name, ext)

    with open(pmid_file, "r") as file_handler, open(new_file,
                                                    "w") as file_writer:
        for line in file_handler:
            if not is_doi(line):
                output = os.popen('php search_pmcid_from_pmid.php %s' %(
                    line)).read()
                if not_found(output):
                    file_writer.write(line)
                else:
                    file_writer.write(output)
            else:
                file_writer.write(line)
    return new_file

def file_stats(file_name: str) -> None:
    """This function gives some statistics about a given file of articles,
    the percentage of DOI links, PMIDs and PMCIDs.

    Parameters
    ----------
    file_name : str
        The file path to be analyzed.

    Returns
    -------
    None
        Prints out some statistics about a file.

    """
    with open(file_name, "r") as file_handler:
        
        n_doi, n_pmid, n_pmcid, lines = 0, 0, 0, 0
        for line in file_handler:
            lines += 1
            if is_doi(line):
                n_doi += 1
            elif is_pmc(line):
                n_pmcid += 1
            else:
                n_pmid += 1
        doi = "doi = %s/%s (%.2f%%)\n" %(n_doi, lines, n_doi/lines*100)
        pmid = "PMID = %s/%s (%.2f%%)\n" %(n_pmid, lines, n_pmid/lines*100)
        pmcid = "PMCID = %s/%s (%.2f%%)\n" %(n_pmcid, lines, n_pmcid/lines*100)
        print(doi, pmid, pmcid)
        
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

def generate_wordcloud(long_str: str) -> WordCloud:
    """A function to generate a wordcloud for a given dataset.

    Parameters
    ----------
    long_str : str
        The dataset in a form of a long string.

    Returns
    -------
    WordCloud
        The given WordCloud object.

    """

    wordcloud = WordCloud(background_color="white",
                          max_words=5000,
                          contour_width=3,
                          contour_color='steelblue',
                          width=720,
                          height=360)
    wordcloud.generate(long_str)

    return wordcloud
