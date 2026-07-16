from schemas.report_issue import ReportIssueRequest

from utils.email import (
    send_support_email,
    send_support_confirmation,
)


def report_issue_service(
    request: ReportIssueRequest,
):

    full_message = f"""
Issue Category:
{request.category}

-----------------------------------------

Issue Title:
{request.title}

-----------------------------------------

Description:

{request.description}
"""

    send_support_email(
        user_email=request.email,
        subject=f"[Bug Report] {request.title}",
        message_text=full_message,
    )

    send_support_confirmation(
        receiver_email=request.email,
    )

    return {
        "message": "Issue reported successfully."
    }