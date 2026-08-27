import uuid

from sqlalchemy import text
from database import SessionLocal


def save_lab_results(
    patient_id,
    document_id,
    labs
):

    db = SessionLocal()

    try:

        for lab in labs:

            reference_range = lab.get(
                "reference_range",
                [None, None]
            )

            reference_low = (
                reference_range[0]
                if reference_range
                else None
            )

            reference_high = (
                reference_range[1]
                if reference_range
                else None
            )

            db.execute(
                text("""
                    INSERT INTO lab_results
                    (
                        result_id,
                        patient_id,
                        document_id,
                        test_name,
                        test_category,
                        value,
                        unit,
                        reference_low,
                        reference_high,
                        abnormal_flag,
                        result_date
                    )
                    VALUES
                    (
                        :result_id,
                        :patient_id,
                        :document_id,
                        :test_name,
                        :test_category,
                        :value,
                        :unit,
                        :reference_low,
                        :reference_high,
                        :abnormal_flag,
                        :result_date
                    )
                """),
                {
                    "result_id": str(uuid.uuid4()),

                    "patient_id": patient_id,

                    "document_id": document_id,

                    "test_name": lab["test_name"],

                    "test_category": "LAB",

                    "value": lab.get("value"),

                    "unit": lab.get("unit"),

                    "reference_low": reference_low,

                    "reference_high": reference_high,

                    "abnormal_flag": lab.get(
                        "abnormal",
                        False
                    ),

                    "result_date": lab.get("date")
                }
            )

        db.commit()

        print(
            f"✅ Saved {len(labs)} lab results"
        )

    except Exception as e:

        db.rollback()

        print(
            "❌ Failed to save lab results:",
            e
        )

        raise

    finally:

        db.close()