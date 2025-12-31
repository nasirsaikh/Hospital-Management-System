from ext import mail
from flask_mail import Message


def send_email(to, subject, body, attachments=None, cc=None, bcc=None):
    """
    Send an email with optional attachments.

    attachments format:
        [
            ("filename.csv", file_bytes, "text/csv"),
            ("report.pdf", pdf_bytes, "application/pdf")
        ]
    """

    msg = Message(
        subject=subject,
        recipients=[to] if isinstance(to, str) else to,
        cc=cc,
        bcc=bcc,
        html=body
    )

    if attachments:
        for filename, file_bytes, mime in attachments:
            msg.attach(
                filename=filename,
                content_type=mime,
                data=file_bytes
            )

    mail.send(msg)
