import re
import smtplib

from email.mime.text import MIMEText
from dundie.settings import SMTP_HOST, SMTP_PORT, SMTP_TIMEOUT
from dundie.utils.log import get_logger

log = get_logger()

EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


def check_valid_email(address):
    """Check if an email address is valid.

    Returns: True if valid, False otherwise.
    """
    return bool(re.fullmatch(EMAIL_REGEX, address))


def send_email(from_, to, subject, body):
    if not isinstance(to, list):
        to = [to]

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT) as server:
            message = MIMEText(body)
            message["From"] = from_
            message["To"] = ",".join(to)
            message["Subject"] = subject
            server.sendmail(from_, to, message.as_string())
    except Exception:
        log.error("Error sending email to %s", ", ".join(to))
