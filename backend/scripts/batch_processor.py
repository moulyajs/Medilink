import os
from app import ocr_process, extract_entities, ner_entities, extract_medicines, generate_summary

data_folder = "../data"
for file in os.listdir(data_folder):
    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.pdf')):
        path = os.path.join(data_folder, file)
        text, top_lines = ocr_process(path)
        entities = extract_entities(text, top_lines)
        ner = ner_entities(text)
        if ner['organizations']:
            entities['hospital'] = ner['organizations'][0]
        medicines = extract_medicines(text)
        summary = generate_summary(entities, medicines)
        print(f"\nFILE: {file}")
        print("FINAL ENTITIES:", entities)
        print("SUMMARY:", summary)
