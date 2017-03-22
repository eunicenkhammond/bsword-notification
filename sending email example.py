#!/usr/bin/python3 
import smtplib
content = 'example email stuff here'

mail = smtplib.SMTP('smtp.gmail.com',587)

mail.ehlo()

mail.starttls()

mail.login('bswordnotification@gmail.com' , 'notification301')

mail.sendmail('bswordnotification@gmail.com','siya12896@gmail.com',content)

mail.close()