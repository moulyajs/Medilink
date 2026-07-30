import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


# ----------------------------------------
# OTP Email
# ----------------------------------------
def send_otp_email(receiver_email: str, otp: str):

    message = MIMEMultipart()

    message["From"] = SMTP_EMAIL
    message["To"] = receiver_email
    message["Subject"] = "Medilink Email Verification"

    body = f"""
Hello,

Your Medilink OTP is:

{otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.

Thank you,
Medilink
"""

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    ) as server:

        server.starttls()

        server.login(
            SMTP_EMAIL,
            SMTP_PASSWORD
        )

        server.sendmail(
            SMTP_EMAIL,
            receiver_email,
            message.as_string()
        )


# ----------------------------------------
# Support Email
# ----------------------------------------
def send_support_email(
    user_email: str,
    subject: str,
    message_text: str
):

    message = MIMEMultipart()

    message["From"] = SMTP_EMAIL
    message["To"] = SMTP_EMAIL
    message["Subject"] = f"Medilink Support | {subject}"

    body = f"""
New Support Request

---------------------------------------

From:
{user_email}

Subject:
{subject}

---------------------------------------

Message:

{message_text}
"""

    message.attach(
        MIMEText(body, "plain")
    )

    with smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    ) as server:

        server.starttls()

        server.login(
            SMTP_EMAIL,
            SMTP_PASSWORD
        )

        server.sendmail(
            SMTP_EMAIL,
            SMTP_EMAIL,
            message.as_string()
        )


# ----------------------------------------
# Confirmation Email
# ----------------------------------------
def send_support_confirmation(
    receiver_email: str
):

    message = MIMEMultipart()

    message["From"] = SMTP_EMAIL
    message["To"] = receiver_email
    message["Subject"] = "Support Request Received"

    body = """
Hello,

Thank you for contacting Medilink Support.

We have received your request successfully.

Our team will review it and respond as soon as possible.

Regards,
Medilink Support Team
"""

    message.attach(
        MIMEText(body, "plain")
    )

    with smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    ) as server:

        server.starttls()

        server.login(
            SMTP_EMAIL,
            SMTP_PASSWORD
        )

        server.sendmail(
            SMTP_EMAIL,
            receiver_email,
            message.as_string()
        )