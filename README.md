# information-retrieval-spr21
a simple search engine written in python


# About This Project
Phase 1:
Creating a simple information retrieval model
In order to create a simple model, it's necessary to index the documents so that when we received the query, the inverse index is used to retrieve the related
documents.
The steps of this phase of the project are as follows:
1)tokenization
2)inverted index construction
3)stopwords elimination, suffixes elimination, lemmatization, stemming (with at least 20 words in each set)
4)remove words with high frequency
5)respond user query

Phase 2:
Completing the information retrieval model and provide more advanced functionalities
Ranking search results based on their relevance to the user query using vector space and output results are sorted by similarity.
The steps of this phase of the project are as follows:
1)use tf-idf weighting method and index elimination
2)cosine similarity to calculate similarity
3)champion list and select K best scores


# Getting Started
## Prerequisites
- put data.xlsx in your project path
- xlrd

`pip install xlrd`

# License
Distributed under the MIT License. See `LICENSE.txt` for more information

# Contact
rezaie.somayeh79@gmail.com
