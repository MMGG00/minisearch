import re

STOPWORDS = {"or", "a", "is", "and", "of", "to", "in", "it", "that", "was", "the"}


def tokenize(text: str):
    text = text.lower()

    text = text.replace("'", "")
    text = text.replace("\u2019", "")

    return [w for w in re.findall(r"[a-z0-9]+", text) if w not in STOPWORDS]
