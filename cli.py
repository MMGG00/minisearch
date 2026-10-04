import argparse

from search import search
from index import assemble_index
from incremental import update_state
import storage

STATE_FILE = "index.json"


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")

    index_cmd = sub.add_parser("index")
    index_cmd.add_argument("folder")

    query_cmd = sub.add_parser("query")
    query_cmd.add_argument("terms")

    args = parser.parse_args()

    if args.command == "index":
        old_files = storage.load_state(STATE_FILE)
        new_files, stats = update_state(args.folder, old_files)

        changed = stats["added"] + stats["updated"] + stats["removed"]
        if changed:
            storage.save_state(STATE_FILE, new_files)

        print(
            f"{len(new_files)} docs | "
            f"added {stats['added']}, updated {stats['updated']}, "
            f"removed {stats['removed']}, unchanged {stats['unchanged']}"
        )
        if not changed:
            print("Index already up to date.")

    elif args.command == "query":
        files = storage.load_state(STATE_FILE)
        if not files:
            print("No index found. Run: python cli.py index <folder>")
            return

        idx, doc_lengths, paths = assemble_index(files)
        results = search(args.terms, idx, doc_lengths)
        if not results:
            print("No results")
        for doc_id, score in results:
            print(paths[doc_id], round(score, 3))


if __name__ == "__main__":
    main()