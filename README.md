# CAZy's little helper

<!-- 
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dnazip-bioinfo?color=green)
![PyPI](https://img.shields.io/pypi/v/dnazip-bioinfo?color=green)
-->
[![forthebadge](https://forthebadge.com/images/badges/open-source.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/reading-6th-grade-level.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-black-magic.svg)](https://forthebadge.com)
![package graphix](graphix.png)

> A **model** to predict the **compatibility** of scientific literature with the [CAZy database](http://www.cazy.org/), the endgoal would be to ***assist biocurators*** by giving a score of **confidence** for each article that asseses its compatibility with certain criteria needed to integrate the database.

## Analysis pipeline

- List of **PMIDs** &#8594; **PMCIDs** (if available otherwise leave it as a PMID) &#8594; **Full text** (if available can be scraped with Bilbio otherwise get only the abstract via eutils) &#8594; Text **preprocessing** &#8594; **TF-IDF** &#8594; A calibrated Support Vector Machine **classifier** &#8594; A confidence **score**

## Installation

- The package can be installed either from pip or from the source code hosted on github.

### With pip

```bash
pip install cazy-little-helper
```

### From source

```bash
git clone https://github.com/dabane-ghassan/cazy-little-helper.git
cd cazy-little-helper
sudo python3 setup.py install
```
## Updating

```bash
pip install cazy-little-helper --upgrade
```

## Getting started

- Insert some neat explanations and commands to see how it works.

## How CAZy's little helper was built

- That curious? Welcome 😊, you'll be well satisfied [here](https://github.com/dabane-ghassan/cazy-little-helper/blob/main/results/analysis.md).

## TODO: The future of CAZy's little helper

- Building a Deep learning model and benchmarking against the classical TF-IDF-SVM machine learning approach. 
  > LDA &#8594; Word2Vec &#8594; BERT 

- Build an API and deploy the model to facilitate its usage.

## About

> This project was a part of a 2-months internship at the Architecture et Fonction des Macromolécules Biologiques laboratory [(AFMB, Marseille, France)](http://www.afmb.univ-mrs.fr/), hosted within the [Glycogenomics](http://www.afmb.univ-mrs.fr/glycogenomique,39) team.

### Acknowledgements

> First, I would like to start by thanking [Dr. Nicolas Terrapon](http://www.afmb.univ-mrs.fr/Nicolas-Terrapon?lang=fr) for his patience, precious help and invaluable supervision, not to mention the oppurtunity that he gave me to work on such an interesting project. In addition, I would like to deeply thank [Dr. Philippe Ortet](https://www.linkedin.com/in/philippe-ortet-23759a7b/?originalSubdomain=fr) for his precious ideas, wonderful insights and his guidance and expertise that helped me easily navigate and use various complex subjects throughout the projet. Last but not least, I would like to finish by thanking all the Glycogenomics team for their appreciable hospitality.

### :scroll: License 
**MIT Licensed** © [Ghassan Dabane](https://github.com/dabane-ghassan), 2021.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![forthebadge](https://forthebadge.com/images/badges/made-with-markdown.svg)](https://forthebadge.com)
[![ForTheBadge uses-git](http://ForTheBadge.com/images/badges/uses-git.svg)](https://GitHub.com/)
[![ForTheBadge uses-badges](http://ForTheBadge.com/images/badges/uses-badges.svg)](http://ForTheBadge.com)
