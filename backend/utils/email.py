import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


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