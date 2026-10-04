import argparse
import json

from loader import load_docs
from index import build_index
from search import search
import storage


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")

    indexCmd = sub.add_parser("index")
    indexCmd.add_argument("folder")

    query = sub.add_parser("query")
    query.add_argument("terms")

    args = parser.parse_args()

    if args.command == "index":
        print("indexing", args.folder)
        docs, paths = load_docs(args.folder)
        idx, docLengths = build_index(docs)
        print("Docs: ", len(docs), "Idx: ", len(idx))

        storage.save_index("index.json", idx, docLengths, paths)

    elif args.command == "query":
        print("searching", args.terms)
        idx, doc_lengths, paths = storage.load_index("index.json")
        results = search(args.terms, idx, doc_lengths)
        if not results:
            print("No Results")
        for doc_id, score in results:
            print("Doc ID: ", paths[doc_id], "Score: ", round(score, 3))


if __name__ == "__main__":
    main()
