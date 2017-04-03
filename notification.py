class NotificationRequest(object):
	def __init__(self, uId, msg, nType):
		self.userId = uId
		self.message = msg
		self.noticeType = nType