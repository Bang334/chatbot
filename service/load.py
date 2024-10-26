import os
from pymongo import MongoClient
from bson import ObjectId
import dotenv
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
db_service = DatabaseService("mongodb+srv://bangkieu936:bangkieu936@cluster0.difgp.mongodb.net/chatbot_db", "chatbot_db")
