from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import json
from notification import NotificationRequest
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

global sendemail
global logNotification

messageLog = []
PORT_NUMBER = 8000

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/demoHTML(testing and working).html"

		try:
			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
                        
        def do_POST(self):
            print "in post method"
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(self.data_string)
            
            #CREATE NEW NOTIFICATION REQUEST OBJECT, with the parameters data['userID'], data['message'], data['noticeType']
                #CALL THE SEND_EMAIL FUNCTION WITH THE OBJECT
            
            notificationRequest = NotificationRequest(data['userID'], data['message'], data['noticeType'])
            self.sendemail(notificationRequest)
            self.logNotification(notificationRequest) 
                
            #create a new json object
            json_data = json.dumps(data)
            
            print 'JSON: ', json_data
            #send the jason object
            self.send_response(200)
            self.send_header('Content-type',"application/x-www-form-urlencoded")
            self.end_headers()
            self.wfile.write(json_data)
            return 

        def sendemail(self, notificationRequest):
            emailTo = notificationRequest.userId
            message = notificationRequest.message
            subject = notificationRequest.noticeType
            
            fromaddr = "bswordnotification@gmail.com"
            toaddr = emailTo
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = notificationRequest.noticeType

            body = notificationRequest.message
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, 'notification301')
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            return
            print("the emails subject is :"+subject)
            print("the emails message is  is :"+message)
            print("the email address that the email is being sent to is "+emailTo)
          #add implementation to send the email
            return
        
        def logNotification(self, notificationRequest):
            messageLog.append(notificationRequest)
            print(messageLog[0].userId)
            return
        
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()