#ner_extraction.py
import spacy

nlp = spacy.load("en_core_web_sm")

def ner_entities(text):
    doc = nlp(text)

    ner_data = {
        "persons": [],
        "organizations": []
    }

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            ner_data["persons"].append(ent.text)
        elif ent.label_ == "ORG":
            ner_data["organizations"].append(ent.text)

    return ner_data
