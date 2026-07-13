from rapidfuzz import fuzz


def verify_patient(user_profile, extracted_patient):
    """
    Verifies whether the uploaded report belongs to the logged-in user.

    Returns:
        {
            "verified": True/False,
            "score": int,
            "reason": str
        }
    """

    # -----------------------------
    # Name
    # -----------------------------
    user_name = (user_profile.get("name") or "").strip().lower()
    report_name = (extracted_patient.get("patient_name") or "").strip().lower()

    name_score = fuzz.partial_ratio(user_name, report_name)

    # -----------------------------
    # Age
    # -----------------------------
    try:
        user_age = int(user_profile.get("age"))
        report_age = int(extracted_patient.get("age"))
        age_match = abs(user_age - report_age) <= 1
    except:
        age_match = False

    # -----------------------------
    # Gender
    # -----------------------------
    user_gender = (user_profile.get("gender") or "").lower()
    report_gender = (extracted_patient.get("gender") or "").lower()

    gender_match = user_gender == report_gender

    # -----------------------------
    # Decision
    # -----------------------------
    if name_score >= 90 and age_match and gender_match:
        return {
            "verified": True,
            "score": name_score,
            "reason": "Patient verified."
        }

    return {
        "verified": False,
        "score": name_score,
        "reason":
            f"Mismatch detected "
            f"(Name Score={name_score}, "
            f"Age Match={age_match}, "
            f"Gender Match={gender_match})"
    }