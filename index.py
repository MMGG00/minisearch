from collections import Counter
from tokenizer import tokenize


def build_index(docs):
    index = {}
    doc_lengths = {}
    for doc_id, text in docs.items():
        tokens = tokenize(text)
        doc_lengths[doc_id] = len(tokens)
        counts = Counter(tokens)
        for word, count in counts.items():
            if word not in index:
                index[word] = []
            index[word].append((doc_id, count))

    return index, doc_lengths
