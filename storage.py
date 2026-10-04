import json


def save_index(filename, idx, doc_lengths, doc_paths):
    data = {
        "index": idx,
        "doc_lengths": doc_lengths,
        "paths": doc_paths,
    }
    with open(filename, "w") as f:
        json.dump(data, f)


def load_index(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    idx = data["index"]
    doc_lengths = {int(k): v for k, v in data["doc_lengths"].items()}
    paths = {int(k): v for k, v in data["paths"].items()}
    return idx, doc_lengths, paths
