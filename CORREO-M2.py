#!/usr/bin/env python
# -*- coding: utf-8 -*-
#CODED BY MATIAS FIGUEROA TAPIA
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import os

#PRIMERO DEFINIMOS SI EXISTE EL ARCHIVO Y SI TIENE CONTENIDO
archivo = 'LOG-BKP-EXPORT-M3.csv'
direccion = "192.141.48.55" #HOST HACIA DONDE VA EL PING
respuesta = os.system("ping -c 3 " + direccion)

if (os.path.isfile(archivo)) and respuesta == 0:

 emailfrom = "monitor.bot.cimple@gmail.com"
 emailto = "ivan.demaria@tecnoaplica.cl"
 fileToSend = "LOG-BKP-EXPORT-M3.csv"
 username = "monitor.bot.cimple@gmail.com"
 password = "cimple123.,/="

 msg = MIMEMultipart()
 msg["From"] = emailfrom
 msg["To"] = emailto
 msg["Subject"] = "ENVIADO DESDE RPI ARCHIVO LOG-BKP-EXPORT-M3.csv"
 msg.preamble = "mensaje automatico envio data LOG-BKP-EXPORT-M3.csv"

 ctype, encoding = mimetypes.guess_type(fileToSend)
 if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

 maintype, subtype = ctype.split("/", 1)

 if maintype == "text":
    fp = open(fileToSend)
    # Note: we should handle calculating the charset
    attachment = MIMEText(fp.read(), _subtype=subtype)
    fp.close()
 elif maintype == "image":
    fp = open(fileToSend, "rb")
    attachment = MIMEImage(fp.read(), _subtype=subtype)
    fp.close()
 elif maintype == "audio":
    fp = open(fileToSend, "rb")
    attachment = MIMEAudio(fp.read(), _subtype=subtype)
    fp.close()
 else:
    fp = open(fileToSend, "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
 attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
 msg.attach(attachment)

 server = smtplib.SMTP("smtp.gmail.com:587")
 server.starttls()
 server.login(username,password)
 server.sendmail(emailfrom, emailto, msg.as_string())
 server.quit()
 ###eliminar despues de 7 dias utilizar crontab
 os.remove("LOG-BKP-EXPORT-M3.csv")
 print("ARCHIVO LOG-BKP-EXPORT-M3.csv BORRADO...")
else:

    print("..NO HAY RESPUESTA DEL HOST O EL ARCHIVO NO ESTA ..!!")