import smtplib
from socket import gaierror
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
import base64


class SMTPClient:
    def __init__(self, server: str, login: str, pswd: str, sender: str,
                 port: int = 2525):
        self.__port = port
        self.__server = server
        self.__password = pswd
        self.__login = login
        self.__sender = sender
        self.__content = {}

    def add_text_plain(self, plain_path: str):
        with open(plain_path, "r") as file:
            plain_text = MIMEText(file.read(), 'plain')
            self.__content.update({'plain_text': plain_text})

    def add_text_html(self, html_path: str):
        with open(html_path, "r") as file:
            html_text = MIMEText(file.read(), 'html')
            self.__content.update({'html_text': html_text})

    def add_image_html(self, img_path: str):
        with open(img_path, "rb") as file:
            encoded = base64.b64encode(file.read()).decode()
            html_text = f"""\
            <html>
                <body>
                    <img src="data:image/jpg;base64,{encoded}">
                </body>
            </html>
            """
            html_image = MIMEText(html_text, "html")
            self.__content.update({'image': html_image})

    def add_file_attachment(self, file_path: str):
        with open(file_path, "rb") as file:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", f"attachment; filename={file_path}")
            self.__content.update({'attachment': attachment})

    def send_email(self, receiver: str, subject: str):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.__sender
        message["To"] = receiver

        for key in self.__content.keys():
            message.attach(self.__content.get(key))

        server = smtplib.SMTP(self.__server, self.__port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.__login, self.__password)
        server.sendmail(self.__sender, receiver, message.as_string())
        server.close()

        print('Mail has been sent')