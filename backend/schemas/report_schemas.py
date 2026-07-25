"""
schemas/report_schemas.py

Pydantic RESPONSE models for reading data back out of the tables
that already exist and are already being written to:
    documents    (written by scripts/uploader.py)
    lab_results  (written by scripts/record_saver.py)

This does NOT create any new database tables. It just shapes the
JSON that GET /reports/list and GET /reports/{document_id} return.
"""

from datetime import datetime, date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class LabValueResponse(BaseModel):
    result_id: UUID
    test_name: str
    value: float
    unit: Optional[str] = None
    reference_low: Optional[float] = None
    reference_high: Optional[float] = None

    # Stored as PostgreSQL BOOLEAN
    abnormal_flag: Optional[bool] = None

    # Stored as PostgreSQL DATE
    result_date: Optional[date] = None

    class Config:
        from_attributes = True


class ReportSummary(BaseModel):
    document_id: UUID
    document_type: str
    upload_date: datetime

    # Computed in the API
    status: str
    lab_count: int

    class Config:
        from_attributes = True


class ReportDetail(BaseModel):
    document_id: UUID
    document_type: str
    upload_date: datetime

    status: str
    lab_values: List[LabValueResponse]

    class Config:
        from_attributes = True