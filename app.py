import os
import google.generativeai as genai
import dotenv
import json
from flask import Flask, jsonify, request, render_template, session
import copy
from pymongo import MongoClient
from models.chat_history import ChatHistory
from werkzeug.security import generate_password_hash, check_password_hash

client = MongoClient("mongodb+srv://bangkieu936:bangkieu936@cluster0.difgp.mongodb.net/chatbot_db")  
db = client["chatbot_db"]  
chat_history_collection = db["chat_history"]  
account_collection = db["user"]  

dotenv.load_dotenv()

genai.configure(api_key='AIzaSyBflKFS4hmOd34GGlVRcLimFueb_WTnkV4')

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 1024,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="Bạn là một người bạn hỗ trợ tui học về ngôn ngữ python. Bạn đôi khi hài hước, lấy những ví dụ trực quan dễ hiều, gần gủi",
)

chat_session = model.start_chat(history=[])

chat_session_dict = {}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/api/history', methods=['GET'])
def get_history():
    username = session.get('username')  
    if not username:
        return jsonify(history=[]), 401  

    history = chat_history_collection.find({"username": username})  

    history_list = []
    for record in history:
        record.pop('_id', None)
        history_list.append(record)
    return jsonify(history=history_list)

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Hello, World!")

@app.route('/api/message', methods=['POST'])
def receive_message():
    data = request.json
    message = data.get('message', '')
    
    if message:
        user_ip = request.headers.getlist("X-Forwarded-For")[0] if request.headers.getlist("X-Forwarded-For") else request.remote_addr
        username = session.get('username')  
        if username:
            if user_ip not in chat_session_dict:
                chat_session_dict[user_ip] = copy.deepcopy(chat_session)

            print(f"{username} ({user_ip}): {message}")
            response = chat_session_dict[user_ip].send_message(message)
            response_message = response.text
            print(response_message)

            chat_data = ChatHistory({
                "username": username,  
                "message": message,
                "response": response_message
            })
            chat_data.save()  
        else:
            print("User not logged in. Message not saved.")
            response_message = "You need to log in to save chat history."
    else:
        response_message = "No message received"
    
    return jsonify(response=response_message)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(success=False, message="Thiếu thông tin tài khoản hoặc mật khẩu")

    user = account_collection.find_one({"username": username})
    if user and check_password_hash(user['password'], password):
        session['username'] = username  
        return jsonify(success=True, message="Đăng nhập thành công")
    else:
        return jsonify(success=False, message="Sai tài khoản hoặc mật khẩu")

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    print(data)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(success=False, message="Thiếu thông tin tài khoản hoặc mật khẩu")

    existing_user = account_collection.find_one({"username": username})
    if existing_user:
        return jsonify(success=False, message="Tên tài khoản đã tồn tại")

    hashed_password = generate_password_hash(password)
    account_collection.insert_one({"username": username, "password": hashed_password})

    return jsonify(success=True, message="Đăng ký thành công")

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    print("User logged out")  # Thêm dòng này để debug
    return jsonify(success=True, message="Đăng xuất thành công")



if __name__ == '__main__':
    app.secret_key = os.urandom(24)  
    app.run(debug=True)
