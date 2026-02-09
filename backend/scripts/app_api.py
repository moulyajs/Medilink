from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

# Import your existing logic
from ocr_pipeline import ocr_process
from demographics_extraction import extract_demographics
from medicine_extraction import extract_medicines
from lab_extraction import extract_lab_results
from clinical_summary import generate_summary
from clinical_facts_extraction import extract_clinical_facts

app = Flask(__name__)
CORS(app) # Allows React to communicate with Flask

UPLOAD_FOLDER = 'data/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/process', methods=['POST'])
def process_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(file_path)

    # Execute your existing pipeline
    lines, top_lines, doc_type = ocr_process(file_path)
    demographics = extract_demographics(lines, doc_type)
    medicines = extract_medicines(lines)
    lab_results = extract_lab_results(lines) if doc_type == "lab_report" else []
    
    full_text = "\n".join(l["text"] for l in lines)
    clinical_facts = extract_clinical_facts(full_text)
    
    summary = generate_summary(demographics, medicines, lab_results, clinical_facts)

    return jsonify({
        "doc_type": doc_type,
        "demographics": demographics,
        "medicines": medicines,
        "lab_results": lab_results,
        "clinical_facts": clinical_facts,
        "summary": summary
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)