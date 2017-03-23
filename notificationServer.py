from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import json
import datetime
import NotificationRequest

PORT_NUMBER = 8000

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/demoHTML.html"

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
            #notificationRequest = NotificationRequest(data['userID'], data['message'], data['noticeType'])
            #notificationRequest = NotificationRequest("test", "test", "test")
            #sendEmail(notificationRequest)

            #new_data = {}
            #new_data['userID'] = data['userID']
            #new_data['message'] = data['message']
            #new_data['noticeType'] = data['noticeType']
                
                
            #create a new json object
            json_data = json.dumps(data)
            
            print 'JSON: ', json_data
            #send the jason object
            self.send_response(200)
            self.send_header('Content-type',"application/x-www-form-urlencoded")
            self.end_headers()
            self.wfile.write(json_data)
            return 

        def send_Email(notificationRequest):
          #to implement
          return
	
	def log_message(notifactionRequest):
	  #to implement
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
