from pymongo import MongoClient
from bson import ObjectId
import datetime

class ChatHistory:
    def __init__(self, data):
        self.username = data['username']
        self.message = data['message']
        self.response = data['response']
        self.session_id = data.get('session_id', str(ObjectId()))

    def save(self):
        db = MongoClient("mongodb+srv://bangkieu936:bangkieu936@cluster0.difgp.mongodb.net/chatbot_db")["chatbot_db"]
        collection = db["chat_history"]

        existing_session = collection.find_one({"username": self.username, "session_id": self.session_id})
        new_conversation = [
            {"role": "user", "parts": self.message},
            {"role": "model", "parts": self.response}
        ]
        
        if existing_session:
            collection.update_one(
                {"username": self.username, "session_id": self.session_id},
                {"$push": {"conversation": {"$each": new_conversation}}}
            )
        else:
            collection.insert_one({
                "username": self.username,
                "session_id": self.session_id,
                "conversation": new_conversation,
                "timestamp": datetime.datetime.utcnow()
            })
