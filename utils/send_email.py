import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from smtplib import SMTP
from utils.printcmd import print_cmd

class Email:
    def __init__(self):
        self.host = 'smtp.gmail.com'
        self.port = 587
        self.email = os.getenv("EMAIL_USER", "")
        self.senha = os.getenv("EMAIL_PASS", "")

    def send(self, title, html, mail_to, anexos=None):
        server = SMTP(self.host, self.port)
        server.ehlo()
        server.starttls()
        server.login(self.email, self.senha)

        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = mail_to
        msg['Subject'] = title

        msg.attach(MIMEText(html, 'html', 'utf-8'))

        if anexos:
            for arquivo in anexos:
                with open(arquivo, 'rb') as f:
                    parte = MIMEBase('application', 'octet-stream')
                    parte.set_payload(f.read())
                    encoders.encode_base64(parte)
                    parte.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{arquivo.split("/")[-1]}"'
                    )
                    msg.attach(parte)

        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print_cmd('Enviado')
