from pathlib import Path


def load_docs(folder):
    docs = {}
    paths = {}
    files = sorted(Path(folder).glob("*.txt"))
    for doc_id, file in enumerate(files):
        docs[doc_id] = file.read_text(encoding="utf-8", errors="ignore")
        paths[doc_id] = str(file)
    return docs, paths
