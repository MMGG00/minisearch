import math
from tokenizer import tokenize


def search(query, index, doc_lengths, k1=1.5, b=0.75):
    N = len(doc_lengths)
    avgdl = sum(doc_lengths.values())/N
    scores = {}
    for word in tokenize(query):
        if word not in index:
            continue
        postings = index[word]
        n = len(postings)
        idf = math.log(1 + (N - n + 0.5) / (n + 0.5))
        for doc_id, tf in postings:
            dl = doc_lengths[doc_id]
            term_score = idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avgdl))
            scores[doc_id] = scores.get(doc_id, 0) + term_score

    return sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
