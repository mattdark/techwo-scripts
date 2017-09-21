#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from maildata import fromaddr, password
import xlrd

def send_mail(email):
    filename = "invitacion_ponencia.docx"
    toaddr = email

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Invitación Meetup TechWo"

    body = """\
    <html>
      <head></head>
      <body>"""

    with open('message', 'r') as mymessage:
        body += mymessage.read().replace('\n', '')

    body += """</body>
    </html>
    """

    msg.attach(MIMEText(body, 'html'))

    attachment = open("./invitation/" + filename, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
