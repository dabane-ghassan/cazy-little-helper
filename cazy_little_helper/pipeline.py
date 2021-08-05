#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 10:54:33 2021

@author: ghassan
"""
from __future__ import absolute_import
from typing import Optional
import os
import numpy as np
import pandas as pd
from metapub.pubmedcentral import get_pmcid_for_otherid
from scraper import Scraper
from preprocessor import Preprocessor
from scorer import Scorer
from toolkit import Toolkit

class Pipeline:

    def __init__(
        self: object,
        input_data: str,
        id_pos: Optional[int]=0,
        biblio_address: Optional[str]="http://localhost/Biblio"
    ) -> None:

        self.input_data = input_data
        self.id_pos = id_pos
        self.output_data = "%s_confidence.csv" % (os.path.splitext(
            self.input_data)[0])
        self.scraper = Scraper(self.input_data, biblio_address)
        self.preprocessor = Preprocessor()
        self.scorer = Scorer()

    def run(
        self: object
    ) -> None:

        print("Reading the file and parsing all available IDs")
        df = pd.read_csv(self.input_data, header=None)
        ids = df[self.id_pos].dropna()

        print("Trying to find PMCIDs...")
        pmcids = ids.apply(lambda idi: pmcid if (
            pmcid := get_pmcid_for_otherid(idi)
            ) else "not found")
        df_data = pd.DataFrame(
            {"id" : ids, "pmcid": pmcids}
            ).sort_values("pmcid").reset_index(drop=True)

        print("Scraping articles...")
        self.scraper.scrape_biblio(
            df_data.loc[df_data.pmcid.apply(
                lambda pmc: Toolkit.is_pmc(pmc)
                ), 'pmcid'])
        self.scraper.fetch_abstracts(
            df_data.loc[(df_data.pmcid.apply(
                lambda pmc: not Toolkit.is_pmc(pmc))
                & df_data.id.astype(str).apply(
                    lambda pmid: not Toolkit.is_doi(pmid))),'id']
            )

        print("Parsing scraped documents...")
        df_data_text = pd.read_csv(self.scraper.text_dataset)
        df_data_text  = df_data_text.fillna('')
        df_data_text["docs"] = df_data_text["title"] + " " + \
            df_data_text["text"]
        df_data_text.drop(['title','text','only_abstract'],
                          inplace=True, axis=1)

        print("Preprocessing documents...")
        self.preprocessor.docs = df_data_text.docs.to_list()
        df_data_words = self.preprocessor.pipeline()

        print("Predicting confidence score...")
        self.scorer.docs = np.array([" ".join(doc) for doc in df_data_words])
        df_data_text['%confidence'] = self.scorer.confidence()

        print("Building the final beautiful results table...")
        df_data['%confidence'] = [df_data_text[
            df_data_text.id == pmc]['%confidence'].values[0]
    if pmc in df_data_text.id.to_list() else "None" for pmc in df_data.pmcid]

        df_data.loc[(df_data['pmcid'] == "not found"), '%confidence'] = [
    df_data_text[df_data_text.id == pmid]['%confidence'].values[0] if pmid
    in df_data_text.loc[(df_data_text.id.apply(
        lambda x: not Toolkit.is_pmc(x))), "id"].to_list() else "None"
    for pmid in df_data.loc[(df_data['pmcid'] == "not found"),
                              'id'].astype(str)
        ]

        new_df = df_data.loc[pd.to_numeric(
            df_data['%confidence'], errors='coerce').sort_values(
    ascending=False).index].reset_index(drop=True)

        print("Table saved to %s" % (self.output_data))
        new_df.to_csv(self.output_data, index=False)
