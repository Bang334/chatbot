# 
from bson import ObjectId
import datetime

class ChatHistory:
    def __init__(self, username, message, response, session_id=None):
        self.username = username
        self.message = message
        self.response = response
        self.session_id = session_id or str(ObjectId())
        self.timestamp = datetime.datetime.utcnow()
