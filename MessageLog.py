"""Get Message with given ID.
"""

import base64
import email
from apiclient import errors

class MessageLog:
  def __init__(self, msgID, labeLID, threadID):
    self.emailAddr = emailAddr
    self.msgID = msgID
    self.labeLID = labeLID
    self.threadID = threadID
    
  def GetMessage(service, user_id, msg_id):
  #  """Get a Message with given ID.

  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    print 'Message snippet: %s' % message['snippet']

    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

    #"""Get a list of Messages from the user's mailbox.

  def ListMessagesMatchingQuery(service, user_id, query=''):
  #"""List all Messages of the user's mailbox matching the query.

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

  try:
    response = service.users().threads().list(userId=user_id,
                                              labelIds=label_ids).execute()
    threads = []
    if 'threads' in response:
      threads.extend(response['threads'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().threads().list(userId=user_id,
                                                labelIds=label_ids,
                                                pageToken=page_token).execute()
      threads.extend(response['threads'])

    return threads
  except errors.HttpError, error:
    print 'An error occurred: %s' % error