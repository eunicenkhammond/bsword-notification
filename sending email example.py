#!/usr/bin/python3 
import notificationRequest.py
import smtplib

content = createNotification('bswordnotification@gmail.com','testing notification mockup')

def sendmail(notificationRequest)
	mail = smtplib.SMTP('smtp.gmail.com',587)

	mail.ehlo()

	mail.starttls()

	mail.login('bswordnotification@gmail.com' , 'notification301')

	mail.sendmail('bswordnotification@gmail.com','u15289347@tuks.co.za',content)

	mail.close()
