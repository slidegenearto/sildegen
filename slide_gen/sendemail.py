import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
from .constants import SEND_GRID_KEY

def send_email_with_attachment(from_email,to_emails,subject,html_content,filepath):
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content)
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()

        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName('attachment.pptx'),
            FileType('application/pptx'),
            Disposition('attachment')
        )
        message.attachment = attachedFile
        sg = SendGridAPIClient(SEND_GRID_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return response.status_code
    except Exception as e:
        print(e.message)
        return e.message