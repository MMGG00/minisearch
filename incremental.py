from pathlib import Path

from index import index_document


def update_state(folder, old_files):
    """Compare the folder to the saved state and only re-process what changed.

    old_files: the saved state, {path: {"id", "mtime", "size", "length", "counts"}}
    returns: (new_files, stats)
    """
    new_files = {}
    stats = {"added": 0, "updated": 0, "unchanged": 0, "removed": 0}

    # new files get ids above every id we've ever handed out, so old ids never shift
    next_id = max((record["id"] for record in old_files.values()), default=-1) + 1

    for file in sorted(Path(folder).glob("*.txt")):
        key = str(file)
        info = file.stat()
        old = old_files.get(key)

        # same modified time and same size -> reuse the saved record, don't read the file
        if old is not None and old["mtime"] == info.st_mtime and old["size"] == info.st_size:
            new_files[key] = old
            stats["unchanged"] += 1
            continue

        text = file.read_text(encoding="utf-8", errors="ignore")
        length, counts = index_document(text)

        if old is not None:
            doc_id = old["id"]
            stats["updated"] += 1
        else:
            doc_id = next_id
            next_id += 1
            stats["added"] += 1

        new_files[key] = {
            "id": doc_id,
            "mtime": info.st_mtime,
            "size": info.st_size,
            "length": length,
            "counts": counts,
        }

    # anything saved before that is no longer in the folder was deleted
    stats["removed"] = len(set(old_files) - set(new_files))
    return new_files, stats
