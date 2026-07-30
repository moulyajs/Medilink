from fastapi import APIRouter

from schemas.report_issue import (
    ReportIssueRequest,
    ReportIssueResponse,
)

from services.report_issue_service import (
    report_issue_service,
)

router = APIRouter(
    prefix="/support",
    tags=["Support"],
)


@router.post(
    "/report-issue",
    response_model=ReportIssueResponse,
)
def report_issue(
    request: ReportIssueRequest,
):

    return report_issue_service(request)