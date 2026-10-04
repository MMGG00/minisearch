# minisearch

A small command-line search engine written from scratch in Python. It indexes a
folder of `.txt` files and ranks them against a query using BM25.

No third-party dependencies — just the Python 3 standard library.

## Usage

Build an index from a folder of `.txt` files:

```bash
python cli.py index books
```

```
indexing books
Docs:  5 Idx:  23308
```

`Docs` is the number of files indexed and `Idx` is the number of unique words.
The index is saved to `index.json` in the current directory.

Search the saved index:

```bash
python cli.py query "white whale"
```

```
searching white whale
Doc ID:  books\moby_dick.txt Score:  2.399
Doc ID:  books\frankenstein.txt Score:  1.78
...
```

Results are listed from best to worst match. If nothing matches, it prints
`No Results`.

> On Windows, if `python` opens the Microsoft Store, use `py` instead
> (e.g. `py cli.py index books`).

## How it works

1. **Load** (`loader.py`) — reads every `*.txt` file in the folder (not
   subfolders) as UTF-8, skipping undecodable bytes. Files are sorted by name
   and numbered from 0.
2. **Tokenize** (`tokenizer.py`) — lowercases the text, removes apostrophes
   (so `don't` becomes `dont`), splits on anything that isn't a letter or
   digit, and drops a small stopword list:
   `a, and, in, is, it, of, or, that, the, to, was`.
3. **Index** (`index.py`) — builds an inverted index mapping each word to a
   list of `(doc_id, count)` pairs, plus the length of each document in tokens.
4. **Store** (`storage.py`) — saves the index, document lengths and file paths
   to `index.json`, and loads them back for queries.
5. **Search** (`search.py`) — tokenizes the query the same way and scores each
   document with BM25 (`k1 = 1.5`, `b = 0.75`). Scores for multiple query words
   are added together, so a document only needs to contain one of them to
   appear in the results.

## Project layout

| File | Purpose |
|---|---|
| `cli.py` | Command-line entry point (`index` and `query` commands) |
| `loader.py` | Reads `.txt` files from a folder |
| `tokenizer.py` | Text normalization and stopword removal |
| `index.py` | Builds the inverted index |
| `search.py` | BM25 ranking |
| `storage.py` | Saves/loads `index.json` |

## Limitations

- Only `.txt` files directly inside the given folder are indexed.
- `query` always reads `index.json` from the current directory, so run
  `index` first, from the same directory.
- Searching for only stopwords (e.g. `the`) returns `No Results`.
- No stemming: `whale` and `whales` are different words.
- Words that appear in every document get almost no weight, so very common
  words don't separate results well.
- All results are printed; there is no top-N limit.
