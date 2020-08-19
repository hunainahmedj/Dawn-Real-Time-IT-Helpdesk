import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from scheduler.models import EmailCreds


class Email:

    def __init__(self, recipient, subject, body):
        self.sender_email = EmailCreds.objects.first().email
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.password = EmailCreds.objects.first().password

    def send_mail(self):

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.recipient
        message["Subject"] = self.subject

        # Add body to email
        message.attach(MIMEText(self.body, "plain"))

        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(EmailCreds.objects.first().smtp_server, int(EmailCreds.objects.first().port), context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.recipient, text)