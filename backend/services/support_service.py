from utils.email import (
    send_support_email,
    send_support_confirmation,
)

from schemas.support import ContactSupportRequest


def contact_support_service(
    request: ContactSupportRequest,
):

    send_support_email(
        user_email=request.email,
        subject=request.subject,
        message_text=request.message,
    )

    send_support_confirmation(
        receiver_email=request.email,
    )

    return {
        "message": "Support request sent successfully."
    }