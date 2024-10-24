# models/chat_history.py
from pymongo import MongoClient
import datetime
class ChatHistory:
    def __init__(self, data):
        self.username = data['username']
        self.message = data['message']
        self.response = data['response']

    def save(self):
        client = MongoClient("mongodb+srv://bangkieu936:bangkieu936@cluster0.difgp.mongodb.net/chatbot_db")
        db = client["chatbot_db"]
        collection = db["chat_history"]
        
        # Lưu dữ liệu vào collection
        collection.insert_one({
            "username": self.username,  # Thay IP bằng username
            "message": self.message,
            "response": self.response,
            "timestamp": datetime.datetime.utcnow()  # Lưu thời gian nếu cần
        })
