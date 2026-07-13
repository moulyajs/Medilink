from sqlalchemy import text
from database import SessionLocal
from rapidfuzz import fuzz


def is_same_test(a, b):
    if not a or not b:
        return False

    return fuzz.partial_ratio(
        a.lower().strip(),
        b.lower().strip()
    ) >= 90


def is_duplicate_report(patient_id, current_labs):
    """
    Checks whether the uploaded report already exists.

    Strategy:
    1. Get every previous document of the patient.
    2. Compare uploaded report against each document.
    3. If any document matches >=80%, return True.
    """

    db = SessionLocal()

    # ----------------------------
    # Get all previous documents
    # ----------------------------
    documents = db.execute(
        text("""
            SELECT DISTINCT document_id
            FROM lab_results
            WHERE patient_id = :pid
        """),
        {
            "pid": patient_id
        }
    ).fetchall()

    if not documents:
        db.close()
        return False

    # -----------------------------------
    # Compare with every previous report
    # -----------------------------------
    for doc in documents:

        rows = db.execute(
            text("""
                SELECT test_name, value
                FROM lab_results
                WHERE document_id = :doc
                AND value IS NOT NULL
            """),
            {
                "doc": doc.document_id
            }
        ).fetchall()

        matched = 0

        for lab in current_labs:

            if lab.get("value") is None:
                continue

            for row in rows:

                if row.value is None:
                    continue

                if is_same_test(lab["test"], row.test_name):

                    if abs(float(lab["value"]) - float(row.value)) < 0.0001:

                        matched += 1
                        break

        similarity = matched / max(
            len(rows),
            len(current_labs),
            1
        )

        print("\n========== DUPLICATE CHECK ==========")
        print("Document ID   :", doc.document_id)
        print("Stored Tests  :", len(rows))
        print("Current Tests :", len(current_labs))
        print("Matched       :", matched)
        print("Similarity    :", f"{similarity*100:.2f}%")
        print("====================================")

        if similarity >= 0.80:

            db.close()
            return True

    db.close()

    return False