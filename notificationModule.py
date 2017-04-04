from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from apiclient import errors
#from os import curdir, sep
import nsq
import json
import smtplib
import tornado.ioloop

global sendemail
global logNotification

messageLog = []

#This class will handles any incoming request from
#the browser 
class NotificationRequest():

        def sendEmail(request):
            reqObj = json.loads(request)
            emailTo = reqObj.content.email
# Could maybe be customized if we accept extra parameters
            subject = "NavUP Notification"
            
            fromaddr = "bswordnotification@gmail.com"
            toaddr = emailTo
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = notificationRequest.noticeType

            body = reqObj.content.message
            msg.attach(MIMEText(body, 'plain'))
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login(fromaddr, 'notification301')
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                writer.pub(reqObj.src, '{"src"  : "Notification", "dest" : "'+reqObj.src+'", "msgType" : "response", "queryType" : "", "content" : { "success" : "true", "error" : ""}}')
            except errors.HttpError as err:
                writer.pub(reqObj.src, '{"src"  : "Notification", "dest" : "'+reqObj.src+'", "msgType" : "response", "queryType" : "", "content" : { "success" : "false", "error" : "Error: '+err+'"}}')

            return
        
        def logNotification(self, notificationRequest):
            messageLog.append(notificationRequest)
            print(messageLog[0].userId)
            return
        
try:
    writer = nsq Writer('127.0.0.1', 4150)
    requestServer = nsq.Reader(message_handler=NotificationRequest.sendEmail(request), lookupd_http_addresses=['http://127.0.0.1:4161'], topic='Notification', channel='NavUP', lookupd_poll_interval=15)
	nsq.run()

except:
    print("NSQ Error! Notifications Module generated a critical server error. Notificaitons module likely offline.")