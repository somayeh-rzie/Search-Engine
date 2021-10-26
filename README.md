# information-retrieval-spr21
a simple search engine written in python


# About This Project
Phase 1: <br />
Creating a simple information retrieval model<br />
In order to create a simple model, it's necessary to index the documents so that when we received the query, the inverse index is used to retrieve the related
documents.<br />
The steps of this phase of the project are as follows:<br />
1)tokenization<br />
2)inverted index construction<br />
3)stopwords elimination, suffixes elimination, lemmatization, stemming (with at least 20 words in each set)<br />
4)remove words with high frequency<br />
5)respond user query<br />

Phase 2:<br />
Completing the information retrieval model and provide more advanced functionalities.<br />
Ranking search results based on their relevance to the user query using vector space and output results are sorted by similarity.<br />
The steps of this phase of the project are as follows:<br />
1)use tf-idf weighting method and index elimination<br />
2)cosine similarity to calculate similarity<br />
3)champion list and select K best scores<br />


# Getting Started
## Prerequisites
- put data.xlsx in your project path
- xlrd
    `pip install xlrd`

# License
Distributed under the MIT License. See `LICENSE.txt` for more information

# Contact
rezaie.somayeh79@gmail.com
