import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
import email

from apiclient import errors

#"""Get Message with given ID.

class MessageLog:
  def __init__(userId, emailAddr, msgResource):
    self.userId = userId
    self.emailAddr = emailAddr
    self.msgID = msgResource.id
    self.labeLID = msgResource.labelIds
    self.threadID = msgResource.threadId
    
  def GetMessage(service, user_id, msg_id):
  #  """Get a Message with given ID.
  #
  #  Args:
  #    service: Authorized Gmail API service instance.
  #    user_id: User's email address. The special value "me"
  #    can be used to indicate the authenticated user.
  #    msg_id: The ID of the Message required.

  #  Returns:
  #    A Message.
  #  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    print 'Message snippet: %s' % message['snippet']

    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


  def GetMimeMessage(service, user_id, msg_id):
  #  """Get a Message and use it to create a MIME Message.
  #
  #  Args:
  #    service: Authorized Gmail API service instance.
  #    user_id: User's email address. The special value "me"
  #    can be used to indicate the authenticated user.
  #    msg_id: The ID of the Message required.

  #  Returns:
  #    A MIME Message, consisting of data from Message.
  #  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()

    print 'Message snippet: %s' % message['snippet']

    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

    mime_msg = email.message_from_string(msg_str)

    return mime_msg
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

    #"""Get a list of Messages from the user's mailbox.

  def ListMessagesMatchingQuery(service, user_id, query=''):
  #"""List all Messages of the user's mailbox matching the query.

  #Args:
    #service: Authorized Gmail API service instance.
    #user_id: User's email address. The special value "me"
    #can be used to indicate the authenticated user.
    #query: String used to filter messages returned.
    #Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  #Returns:
    #List of Messages that match the criteria of the query. Note that the
    #returned list contains Message IDs, you must use get with the
    #appropriate ID to get the details of a Message.
  #"""
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


  def ListMessagesWithLabels(service, user_id, label_ids=[]):
  #  """List all Messages of the user's mailbox with label_ids applied.
  #
  #  Args:
  #    service: Authorized Gmail API service instance.
  #    user_id: User's email address. The special value "me"
  #    can be used to indicate the authenticated user.
  #    label_ids: Only return Messages with these labelIds applied.
  #
  #  Returns:
  #    List of Messages that have all required Labels applied. Note that the
  #    returned list contains Message IDs, you must use get with the
  #    appropriate id to get the details of a Message.
  #  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               labelIds=label_ids).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id,
                                                 labelIds=label_ids,
                                                 pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


  #"""Get a Thread

  def GetThread(service, user_id, thread_id):
  #"""Get a Thread.

  #Args:
  #  service: Authorized Gmail API service instance.
  #  user_id: User's email address. The special value "me"
  #  can be used to indicate the authenticated user.
  #  thread_id: The ID of the Thread required.

  #Returns:
  #  Thread with matching ID.
  #"""
  try:
    thread = service.users().threads().get(userId=user_id, id=thread_id).execute()
    messages = thread['messages']
    print ('thread id: %s - number of messages '
           'in this thread: %d') % (thread['id'], len(messages))
    return thread
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


  #"""Get a list of Threads from the user's mailbox.

  def ListThreadsMatchingQuery(service, user_id, query=''):
  #"""List all Threads of the user's mailbox matching the query.

  #Args:
  #  service: Authorized Gmail API service instance.
  #  user_id: User's email address. The special value "me"
  #  can be used to indicate the authenticated user.
  #  query: String used to filter messages returned.
  #         Eg.- 'label:UNREAD' for unread messages only.

  #Returns:
  #  List of threads that match the criteria of the query. Note that the returned
  #  list contains Thread IDs, you must use get with the appropriate
  #  ID to get the details for a Thread.
  #"""
  try:
    response = service.users().threads().list(userId=user_id, q=query).execute()
    threads = []
    if 'threads' in response:
      threads.extend(response['threads'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().threads().list(userId=user_id, q=query,
                                        pageToken=page_token).execute()
      threads.extend(response['threads'])

    return threads
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


  def ListThreadsWithLabels(service, user_id, label_ids=[]):

  #"""List all Threads of the user's mailbox with label_ids applied.

  #Args:
  #  service: Authorized Gmail API service instance.
  #  user_id: User's email address. The special value "me"
  #  can be used to indicate the authenticated user.
  #  label_ids: Only return Threads with these labelIds applied.

  #Returns:
  #  List of threads that match the criteria of the query. Note that the returned
  #  list contains Thread IDs, you must use get with the appropriate
  #  ID to get the details for a Thread.
  #"""
  try:
    response = service.users().threads().list(userId=user_id,
                                              labelIds=label_ids).execute()
    threads = []
    if 'threads' in response:
      threads.extend(response['threads'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().threads().list(userId=user_id, labelIds=label_ids, pageToken=page_token).execute()
      threads.extend(response['threads'])

    return threads
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
