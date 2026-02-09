import re

def extract_ecg_findings(lines):
    text_lines = [l["text"] for l in lines]
    full_text = " ".join(text_lines)

    ecg = {}

    # ------------------------
    # Heart Rate
    # ------------------------
    hr = re.search(r"HR\s*(\d+)\s*bpm", full_text, re.I)
    if hr:
        ecg["heart_rate_bpm"] = int(hr.group(1))

    # ------------------------
    # Time
    # ------------------------
    time = re.search(r"\b(\d{2}:\d{2}:\d{2})\b", full_text)
    if time:
        ecg["time"] = time.group(1)

    # ------------------------
    # QRS duration
    # ------------------------
    qrs = re.search(r"QRS\s*([\d.]+)\s*s", full_text, re.I)
    if qrs:
        ecg["qrs_duration_sec"] = float(qrs.group(1))

    # ------------------------
    # QT / QTc
    # ------------------------
    qt = re.search(r"([\d.]+s)\s*/\s*([\d.]+s)", full_text)
    if qt:
        ecg["qt_qtc"] = qt.group(1) + " / " + qt.group(2)

    # ------------------------
    # AXIS (if present)
    # ------------------------
    axis = re.search(r"Axes?:?\s*([-\d]+)[°]?\s+([-\d]+)[°]?\s+([-\d]+)", full_text)
    if axis:
        ecg["axis"] = {
            "p": int(axis.group(1)),
            "qrs": int(axis.group(2)),
            "t": int(axis.group(3))
        }

    # ------------------------
    # ECG INTERPRETATION (DYNAMIC)
    # ------------------------
    interpretations = []

    for line in text_lines:
        l = line.lower()

        # skip numeric / parameter lines
        if re.search(r"\d", l) and ("bpm" in l or "qrs" in l or "/" in l):
            continue

        # skip junk
        if len(l) < 4:
            continue

        # keep interpretation-like text
        if any(word in l for word in [
            "tachycardia",
            "block",
            "deviation",
            "abnormal",
            "wave",
            "st",
            "ecg"
        ]):
            interpretations.append(line)

    ecg["interpretation"] = interpretations

    return ecg
