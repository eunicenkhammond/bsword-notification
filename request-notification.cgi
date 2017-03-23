import notification.py

formData = cgi.FieldStorage();
notifyRequest = NotificationRequest(formData.getvalue('userID'), formData.getvalue('notifyMsg'));

def createNotification(sender, subject):
	message = MIMEText(notifyRequest.message)
	# The following value should be changed to fetch an email address associated with a uID
	message['to'] = notifyRequest.userID
	# The following should be our server email address
	message['from'] = sender
	# The following should be the subject of the notification that is sent to this function
	message['subject'] = subject
	return {'raw':base64.urlsafe_b64encode(message.as_string())}