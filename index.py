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


def index_document(text):
    """Process ONE document. Returns (length, {word: count})."""
    tokens = tokenize(text)
    return len(tokens), dict(Counter(tokens))


def assemble_index(files):
    """Turn the per-file records into what search() needs.

    files: {path: {"id": ..., "length": ..., "counts": {...}, ...}}
    returns: (index, doc_lengths, paths)
    """
    index = {}
    doc_lengths = {}
    paths = {}
    for path, record in sorted(files.items(), key=lambda item: item[1]["id"]):
        doc_id = record["id"]
        doc_lengths[doc_id] = record["length"]
        paths[doc_id] = path
        for word, count in record["counts"].items():
            index.setdefault(word, []).append((doc_id, count))
    return index, doc_lengths, paths
