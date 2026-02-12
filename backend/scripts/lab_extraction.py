# lab_extraction.py

from semantic_parser import parse_row
from learning_memory import log_failed


def extract_result_section(lines):

    start_keywords = [
        "investigation",
        "result",
        "reference",
        "complete blood count",
        "cbc"
    ]

    end_keywords = [
        "instrument",
        "interpretation",
        "end of report",
        "thanks",
        "method"
    ]

    start = None
    end = None

    for i, l in enumerate(lines):

        text = l["text"].lower()

        if start is None:
            if any(k in text for k in start_keywords):
                start = i
                continue

        if start is not None and end is None:
            if any(k in text for k in end_keywords):
                end = i
                break

    if start is None:
        return lines

    return lines[start:end]


def is_metadata(text):

    bad = [
        "drlogy", "pathology", "mumbai", "phone",
        "page", "pm", "am", "years", "age", "sex",
        "pid", "sample", "barcode", "mindray",
        "instrument", "address", "road", "email"
    ]

    t = text.lower()

    return any(b in t for b in bad)


def extract_lab_results(lines):

    results = []

    section = extract_result_section(lines)

    for l in section:

        text = l["text"]

        if is_metadata(text):
            continue

        parsed = parse_row(text)

        if not parsed:
            log_failed(text)
            continue

        try:
            value = float(parsed["value"])
        except:
            log_failed(text)
            continue

        results.append({
            "test": parsed["test"],
            "value": value,
            "unit": parsed.get("unit"),
            "reference_range": parsed.get("range"),
            "raw_text": text
        })

    return results
