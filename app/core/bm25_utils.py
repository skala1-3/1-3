from rank_bm25 import BM25Okapi

def build_bm25(corpus):
    tokenized_corpus = [doc.split() for doc in corpus]
    return BM25Okapi(tokenized_corpus)
