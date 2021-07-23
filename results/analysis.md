# The analysis

> *“Above all else, show the data.”* – Edward R. Tufte


| Article source | Number of PMCID articles | Compatibiliy |
| --- | ----------- | ---------- |
| CAZyDB | 1093 | + |
| CAZyDB entries without a function  | 6641 | - |
| [ESTHER DB](http://bioweb.supagro.inra.fr/ESTHER/general?what=index) | 2164 |-|
| [Glycogenomics team publications](http://www.afmb.univ-mrs.fr/team-s-publications)  | 182 |-|
| [KLIFS DB](https://klifs.net/)  | 800 |-|
| [The Database of Sulfatases](http://abims.sb-roscoff.fr/sulfatlas/?execution=e2s1) | 27 |-|
| Publications in PubMed that contain the keyword "CAZyme" before 2010 | 676 |-|

- The [Biblio](https://github.com/TigiGln/Biblio) package was used to scrape full texts from PMCIDs

## Text preprocessing

| | Before| After |
| ---| --- | ----------- |
| **CAZy+** | ![image](https://user-images.githubusercontent.com/69251989/126796776-030a691e-280c-4bcb-a1b0-18e2b7607e61.png)| ![image](https://user-images.githubusercontent.com/69251989/126796840-e5a5eb3a-2b58-4e08-8ade-cad2157280e1.png)|
| **CAZy-** |![image](https://user-images.githubusercontent.com/69251989/126797202-a73717fb-72fc-463c-9703-b465c89dee1a.png)| ![image](https://user-images.githubusercontent.com/69251989/126797150-a8b57118-3dd7-485a-9a5c-05b4bbd2edcc.png)|

## Latent Dirichlet Allocation

### The model

```python
best_lda_model = LatentDirichletAllocation(n_components=10,
                                           learning_decay=0.9,
                                           doc_topic_prior=0.01,
                                           topic_word_prior=0.31,
                                           random_state=42)
```

### Topics wordclouds (Top-15 words)

![image](https://user-images.githubusercontent.com/69251989/126797832-95d65cac-acc9-4f87-9356-2adbb409be6a.png)
![image](https://user-images.githubusercontent.com/69251989/126797877-5bf42e22-9ae2-41c4-9a1b-3463b1292cd5.png)
![image](https://user-images.githubusercontent.com/69251989/126797929-8b65943e-70d6-4eba-b188-d97af2f98b41.png)

### Frequency Distribution of Word Counts in Documents

![image](https://user-images.githubusercontent.com/69251989/126798045-07e9d657-c2a8-46cf-860d-60ee2c21396d.png)

![image](https://user-images.githubusercontent.com/69251989/126798171-4099bd30-dc46-4d6e-99e6-80f6fcc06c71.png)
![image](https://user-images.githubusercontent.com/69251989/126798230-d860a68f-9898-4f81-b196-4d10767e4f8b.png)
![image](https://user-images.githubusercontent.com/69251989/126798270-8ac46a7e-1263-4ce8-96f1-45e6ef8350a0.png)

### Word counts and importance of top topic keywords

![image](https://user-images.githubusercontent.com/69251989/126798533-0e804bec-ea14-4960-9e5d-4b5578af1a92.png)
![image](https://user-images.githubusercontent.com/69251989/126798595-bae43c37-89b4-43b1-9842-ed5dcae15b46.png)

### Topics per document source

![image](https://user-images.githubusercontent.com/69251989/126798721-8e26de3d-6f83-4130-8774-a0d0453fe79f.png)
![image](https://user-images.githubusercontent.com/69251989/126798787-5e7bc044-1a05-4b08-93e4-f7e7762237ea.png)
![image](https://user-images.githubusercontent.com/69251989/126798841-c35bd95e-c3ea-4f40-b3c6-6410994e68b2.png)

### K-means clustering of documents
![image](https://user-images.githubusercontent.com/69251989/126798951-9b6eccef-0ea2-4697-a979-e76716cc7fc1.png)

### LDA model predictions on a few abstracts
![image](https://user-images.githubusercontent.com/69251989/126799168-71b4fc21-76d8-419b-8994-04f2b729dfa0.png)

## TF-IDF/ML Classifier

### ROC

![image](https://user-images.githubusercontent.com/69251989/126799550-865f0bae-2ae9-4b00-bce1-95d4a76d247f.png)


### Confusion matrices

| Validation set| Test set |
| --- | ----------- |
|![image](https://user-images.githubusercontent.com/69251989/126799945-9ced7126-a039-4973-b066-bea4f039cf40.png)| ![image](https://user-images.githubusercontent.com/69251989/126800003-a91122ed-d839-49af-b977-d518cbb0f836.png)|
