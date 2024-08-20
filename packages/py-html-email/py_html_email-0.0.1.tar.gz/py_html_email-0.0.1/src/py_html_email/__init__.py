import os
from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Emailer:
    """
    Emailer object that creates an HTML email and sends via an email service.

    :param sender_email
    :param sender_password
    :param smtp_server
    :param smtp_port
    """
    def __init__(self, sender_email: str, sender_password: str, smtp_server: str, smtp_port: int = 587):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = self._std_servers(smtp_server)
        self.smtp_port = self._std_port(smtp_port)
        self.html_template = Path(__file__).with_name('html_generic.html')

    @staticmethod
    def _std_servers(smtp_server: str):
        match smtp_server:
            case 'office':
                return 'smtp.office365.com'
            case 'gmail':
                return 'smtp.gmail.com'
            case _:
                return smtp_server

    @staticmethod
    def _std_port(new_port: int) -> int:
        if new_port is None:
            return 587
        else:
            return new_port

    def _setup_msg(self, to, subject) -> MIMEMultipart:
        # Create a multipart/mixed parent container.
        msg = MIMEMultipart('mixed')
        msg['From'] = self.sender_email
        msg['To'] = to
        msg['Subject'] = subject
        return msg

    @staticmethod
    def _attachment(msg: MIMEMultipart, attachment_path: str) -> MIMEMultipart:
        part = MIMEBase('application', 'octet-stream')
        with open(attachment_path, 'rb') as file:
            part.set_payload(file.read())

        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
        msg.attach(part)
        return msg

    def _write_html(self, **kwargs) -> MIMEMultipart:
        msg_body = MIMEMultipart('alternative')
        with open(self.html_template, 'r') as f:
            html_content = f.read()

        # Replace placeholders in html_content with kwargs
        for key, value in kwargs.items():
            html_content = html_content.replace(f'{{{{ {key} }}}}', value)
            html_content = html_content.replace(f'{{{{ {key} }}}}', '')

        part2 = MIMEText(html_content, 'html')
        msg_body.attach(part2)
        return msg_body

    def send_email(self, to: str, subject: str, attachment_path: str = None, **kwargs) -> None:
        """

        :param to: email address(s) in a string, comma separated.
        :param subject: Subject line of email
        :param attachment_path: optional attachment
        :key msg_header: Header string of email.
        :key msg_title: Title string of email.
        :key msg_body: Remaining text in body of email
        :key

        Example:

        """
        msg = self._setup_msg(to=to, subject=subject)
        if attachment_path:
            msg = self._attachment(msg=msg, attachment_path=attachment_path)

        # Create a multipart/alternative child container.
        msg_body = self._write_html(**kwargs)

        # Attach the multipart/alternative part to the multipart/mixed message
        msg.attach(msg_body)

        # send the mail
        mailserver = smtplib.SMTP(self.smtp_server, self.smtp_port)
        mailserver.starttls()
        mailserver.login(self.sender_email, self.sender_password)
        mailserver.send_message(msg)
        mailserver.quit()
