import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from baseline_engine import update_patient_baselines

patient_id = "5aadb8cc-0fcc-4ade-bbe1-729ec1e6f30b"

update_patient_baselines(patient_id)

print("Done!")