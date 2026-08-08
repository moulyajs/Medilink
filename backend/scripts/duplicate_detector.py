from sqlalchemy import text
from database import SessionLocal
from rapidfuzz import fuzz
import traceback


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

    try:
        print("1 - entered duplicate detector")

        db = SessionLocal()
        print("2 - session created")

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

        print("3 - documents fetched:", len(documents))

        if not documents:
            db.close()
            return False

        # -----------------------------------
        # Compare with every previous report
        # -----------------------------------
        for doc in documents:
            print("4 - processing doc", doc.document_id)

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

            print("5 - rows fetched:", len(rows))

            matched = 0
            print("6 - about to iterate labs")

            for lab in current_labs:
                print("7 - first lab")
                print(lab)
                print(lab.keys())

                if lab.get("value") is None:
                    continue

                for row in rows:

                    if row.value is None:
                        continue

                    test_name = lab.get("test") or lab.get("test_name")

                    if is_same_test(test_name, row.test_name):
                        print("LAB KEYS:", lab.keys())

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
            print("Similarity    :", f"{similarity * 100:.2f}%")
            print("====================================")

            if similarity >= 0.80:
                db.close()
                return True

        db.close()
        return False

    except Exception:
        traceback.print_exc()
        raise