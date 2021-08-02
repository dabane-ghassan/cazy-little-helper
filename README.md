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

- List of **PMIDs/DOIs** &#8594; **PMCIDs** (if available, otherwise leave it as a PMID) &#8594; **Full text** (if available so can be scraped with Bilbio,  otherwise get only the abstract via eutils) &#8594; **Preprocessing** &#8594; **Representation** &#8594; **Classifying** &#8594; **% Confidence score**.

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

## Under the hood: What is CAZy's little helper?

> CAZy's little helper is a ***TF-IDF/SVM machine learning model***, it uses *Term Frequency - Inverse Document Frequency (TF-IDF)* for text representation and a linear kernel *Support Vector Machine* for classification.

- Performance: 

|  Test dataset | Precision | Recall | f1-score | Support|
| -------  | --------- | -------| ---------| ------ |
| CAZyDB-  | 0.97      |0.98|0.98|1326|
| CAZyDB+  | 0.81      |0.74 |0.77 |135|
|Accuracy |      | |**0.96** |**1461**|
|Macro average |  0.89    |0.86 |0.88 |1461|
|Weighted average |      0.96|0.96 |0.96 |1461|


- Before choosing this particular architecture, a panel of Natural Language Processing (NLP) methods for **text classification** were used and tested based upon the custom-created dataset for the CAZy database; methods ranging from classical text representation tools like **TF-IDF** and **word embeddings** *(Word2Vec)* as well as unsupervised topic modeling using **LDA** *(Latent Dirichlet Allocation)*, to even state-of-the-art deep learning approaches like **BERT** *(Bidirectional Encoder Representation from Transformers)*. Furthermore, all the above approaches were benchmarked on the validation and the test datasets and the ***ROC-AUC curves*** are compared.

<table>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/69251989/127856175-f19dc28c-a50f-4525-859e-005172bd750e.png" width=100></td>
    <th colspan=4>Model</th>
  </tr>
  <tr>
    <th rowspan="3">ROC-AUC curve</th>
    <td> <h4>TF-IDF/SVM</h4> <img src="https://user-images.githubusercontent.com/69251989/127856420-0391a88f-c5af-4e47-9f14-aba5d6a31e5d.png" height=200 width=200></td>
    <td> <h4>LDA/Random Forest</h4><img src="https://user-images.githubusercontent.com/69251989/127857086-25dde5a4-ad14-4727-8bf8-b251d2d3e4e5.png" height=200 width=200></td>
    <td> <h4>Word2Vec/SVM </h4><img src="https://user-images.githubusercontent.com/69251989/127858122-d64389cc-fc16-4d63-8609-29fb00423cb1.png" height=200 width=200></td>
    <td> <h4>BERT </h4><img src="https://user-images.githubusercontent.com/69251989/127849611-f706f698-e278-421e-90d8-0ad5034b25c2.png" height=200 width=200></td>
  </tr>
  <tr>
    <td><h4>TF-IDF/Random Forest</h4><img src="https://user-images.githubusercontent.com/69251989/127861999-bdc1d3b8-eebd-444b-981a-e8e8c13d7f77.png" height=200  width=200></td>
    <td><h4>Ensemble Classifier*</h4> <img src="https://user-images.githubusercontent.com/69251989/127862376-a7e9e0e0-7a54-4801-9982-6e2d99fc3be3.png" height=200 width=200></td>
  </tr>
  <tr>
    <td><h4>TF-IDF/Naive Bayes </h4> <img src="https://user-images.githubusercontent.com/69251989/127862065-3ba00179-037c-41b7-b999-b501c8b720a9.png" height=200  width=200></td>
  </tr>
</table>

***\*A soft-voting classifier which relies upon two models, LDA/Random Forest and TF-IDF/SVM***
- More information about the dataset and methods? You're more than welcome to take a bit more extensive look [here](https://github.com/dabane-ghassan/cazy-little-helper/tree/main/analysis).

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
