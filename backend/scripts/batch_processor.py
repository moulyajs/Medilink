import os
from app import ocr_process, extract_entities, ner_entities, extract_medicines, generate_summary

data_folder = "../data"

for file in os.listdir(data_folder):
    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.pdf')):
        path = os.path.join(data_folder, file)

        text, top_lines, doc_type = ocr_process(path)

        print(f"\nFILE: {file}")
        print("DOCUMENT TYPE:", doc_type)

        if doc_type == "lab_report":
            print("SUMMARY: Laboratory investigation report. No medications prescribed.")
            continue

        entities = extract_entities(text, top_lines)

        ner = ner_entities(text)
        if ner["organizations"]:
            for org in ner["organizations"]:
                if "hospital" in org.lower() or "medical" in org.lower():
                    entities["hospital"] = org
                    break

        medicines = extract_medicines(text)
        summary = generate_summary(entities, medicines)

        print("FINAL ENTITIES:", entities)
        print("SUMMARY:", summary)
