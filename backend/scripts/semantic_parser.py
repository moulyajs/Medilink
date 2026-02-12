# semantic_parser.py

import re
import spacy

nlp = spacy.load("en_core_web_sm")

REGEX = re.compile(
    r"""
    (?P<test>[A-Za-z ()./%+-]{3,}?)\s+
    (?P<value>\d+(\.\d+)?)\s*
    (?P<unit>
        mg/dl|g/dl|mmol/l|ng/ml|%|fl|pg|iu/l|u/l
    )?\s*
    (?P<range>
        \d+(\.\d+)?\s*[-–]\s*\d+(\.\d+)?|
        <\s*\d+(\.\d+)?|
        >\s*\d+(\.\d+)?
    )?
    """,
    re.VERBOSE | re.IGNORECASE
)


def regex_parse(text):

    m = REGEX.search(text)

    if not m:
        return None

    return m.groupdict()


def spacy_fallback(text):

    doc = nlp(text)

    nums = []
    words = []

    for ent in doc.ents:
        if ent.label_ == "CARDINAL":
            nums.append(ent.text)

    for token in doc:
        if token.pos_ in ("NOUN", "PROPN", "ADJ"):
            words.append(token.text)

    if not nums or not words:
        return None

    return {
        "test": " ".join(words),
        "value": nums[0],
        "unit": None,
        "range": None
    }


def parse_row(text):

    r = regex_parse(text)

    if r:
        return r

    return spacy_fallback(text)
