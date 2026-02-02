# scripts/user_review.py

def review_prescriptions(prescriptions):
    """
    Simple CLI-based human-in-the-loop review.
    Allows user to correct extracted prescriptions before storing.
    """

    if not prescriptions:
        print("\nNo prescriptions detected.")
        return prescriptions

    print("\n====== USER REVIEW: PRESCRIPTIONS ======")

    reviewed = []

    for idx, p in enumerate(prescriptions, 1):
        print(f"\nPrescription #{idx}")
        print("-" * 40)

        drug = p.get("drug", "")
        dose = p.get("dose", "")
        freq = p.get("frequency", "")

        print(f"Extracted Drug      : {drug}")
        print(f"Extracted Dose      : {dose}")
        print(f"Extracted Frequency : {freq}")

        # Ask user if they want to edit
        edit = input("Do you want to edit this prescription? (y/n): ").strip().lower()

        if edit == "y":
            new_drug = input(f"Enter correct drug name [{drug}]: ").strip()
            new_dose = input(f"Enter correct dose [{dose}]: ").strip()
            new_freq = input(f"Enter correct frequency [{freq}]: ").strip()

            corrected = {
                "drug": new_drug if new_drug else drug,
                "dose": new_dose if new_dose else dose,
                "frequency": new_freq if new_freq else freq,
                "raw_lines": p.get("raw_lines", [])
            }

            reviewed.append(corrected)

        else:
            # Keep as is
            reviewed.append(p)

    print("\n====== REVIEW COMPLETED ======")
    return reviewed
