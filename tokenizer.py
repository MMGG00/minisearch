import re


def tokenize(text: str):
    tokens = []
    stopWords = {"or", "a", "is", "and", "of", "to", "in", "it", "that", "was", "the"}
    text = text.lower()
    text = text.replace("'", "")

    for word in re.findall(r"[a-z0-9]+", text):
        if word not in stopWords:
            tokens.append(word)
    return tokens
