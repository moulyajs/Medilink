from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import re

MODEL_NAME = "d4data/biomedical-ner-all"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)

ner_pipeline = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"
)

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def clean(text):
    text = text.replace("##", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


# --------------------------------------------------
# ML MEDICAL ENTITY EXTRACTION
# --------------------------------------------------
def extract_medical_entities_ml(text):
    if not text or len(text.strip()) < 5:
        return {"ml_diagnoses": []}

    results = ner_pipeline(text)

    diagnoses = []
    buffer = []

    for r in results:
        label = r["entity_group"]
        word = clean(r["word"])

        # Accept ONLY medically relevant labels
        if label in {"Disease_disorder", "Sign_symptom", "Detailed_description"}:
            buffer.append(word)

        elif label == "Biological_structure":
            # keep anatomy only if part of diagnosis
            buffer.append(word)

        else:
            if buffer:
                diagnoses.append(" ".join(buffer))
                buffer = []

    if buffer:
        diagnoses.append(" ".join(buffer))

    # Normalize common cases
    normalized = set()
    for d in diagnoses:
        if "viral" in d and "fever" in d:
            normalized.add("viral fever")
        elif "upper respiratory" in d and "infection" in d:
            normalized.add("upper respiratory tract infection")
        else:
            normalized.add(d)

    return {
        "ml_diagnoses": sorted(normalized)
    }
