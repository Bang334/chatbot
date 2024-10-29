import os
from pymongo import MongoClient
import dotenv
import datetime

# Load biến môi trường từ file .env
dotenv.load_dotenv()

# Lấy URL từ biến môi trường
# mongo_url = os.getenv('MONGO_URL')

class DatabaseService:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
    
    def get_chat_history(self, username):
        chat_history_collection = self.db["chat_history"]
        history = chat_history_collection.find({"username": username})
        history_list = []
        for record in history:
            history_list.append({
                "session_id": record.get("session_id"),
                "conversation": record.get("conversation", [])
            })
        return history_list

    def find_user(self, username):
        account_collection = self.db["user"]
        return account_collection.find_one({"username": username})

    def insert_user(self, username, hashed_password):
        account_collection = self.db["user"]
        account_collection.insert_one({"username": username, "password": hashed_password})
    def save_chat_history(self, chat_data):
        chat_history_collection = self.db["chat_history"]
        existing_session = chat_history_collection.find_one({
            "username": chat_data.username,
            "session_id": chat_data.session_id
        })
        
        new_conversation = [
            {"role": "user", "parts": chat_data.message},
            {"role": "model", "parts": chat_data.response}
        ]
        
        if existing_session:
            chat_history_collection.update_one(
                {"username": chat_data.username, "session_id": chat_data.session_id},
                {"$push": {"conversation": {"$each": new_conversation}}}
            )
        else:
            chat_history_collection.insert_one({
                "username": chat_data.username,
                "session_id": chat_data.session_id,
                "conversation": new_conversation,
                "timestamp": datetime.datetime.utcnow()
            })
db_service = DatabaseService("mongodb+srv://bangkieu936:bangkieu936@cluster0.difgp.mongodb.net/chatbot_db", "chatbot_db")

