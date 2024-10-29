from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    @staticmethod
    def create_account(username, password):
        client = MongoClient("mongodb+srv://bangkieu936:bangkieu936@cluster0.difgp.mongodb.net/chatbot_db")
        db = client["chatbot_db"]
        collection = db["user"]

        if collection.find_one({"username": username}):
            return False  # Tài khoản đã tồn tại

        collection.insert_one({"username": username, "password": Account(username, password).password})
        return True  # Tạo tài khoản thành công

    @staticmethod
    def validate_account(username, password):
        client = MongoClient("mongodb+srv://bangkieu936:bangkieu936@cluster0.difgp.mongodb.net/chatbot_db")
        db = client["chatbot_db"]
        collection = db["user"]

        user = collection.find_one({"username": username})
        if user and check_password_hash(user['password'], password):
            return True  # Đăng nhập thành công
        return False  # Sai tài khoản hoặc mật khẩu
