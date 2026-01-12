def generate_summary(entities, medicines=None):
    summary = []

    if 'patient_name' in entities:
        summary.append(f"Patient {entities['patient_name']}")

    if 'age' in entities and 'gender' in entities:
        summary.append(f"is a {entities['age']}-year-old {entities['gender']}")

    if 'hospital' in entities:
        summary.append(f"treated at {entities['hospital']}")

    if medicines:
        meds = ', '.join([m['name'] for m in medicines])
        summary.append(f"Prescribed medicines: {meds}")

    return ' '.join(summary) + '.'
