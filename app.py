import os
import google.generativeai as genai
import dotenv
import json
from flask import Flask, jsonify, request, render_template, session
import copy
from models.chat_historyDB import ChatHistory
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from service.dbservice import db_service 

dotenv.load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)
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
    system_instruction="Bạn là một người bạn hỗ trợ học về Python, đôi khi hài hước và lấy ví dụ dễ hiểu."
)
chat_session = model.start_chat(history=[])

app = Flask(__name__)
app.secret_key = os.urandom(24)

chat_session_dict = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/history', methods=['GET'])
def get_history():
    username = session.get('username')
    if not username:
        return jsonify(history=[]), 401  

    history = db_service.get_chat_history(username)  
    return jsonify(history=history)

@app.route('/api/message', methods=['POST'])
def receive_message():
    data = request.json
    message = data.get('message', '')
    if message:
        username = session.get('username')
        if username:
            if username not in chat_session_dict:
                chat_session_dict[username] = copy.deepcopy(chat_session)

            response = chat_session_dict[username].send_message(message)
            response_message = response.text

            session_id = session.get('session_id')
            if not session_id:
                session_id = str(ObjectId())
                session['session_id'] = session_id  

            chat_data = ChatHistory(
                username=username,
                message=message,
                response=response_message,
                session_id=session_id
            )
            db_service.save_chat_history(chat_data)
        else:
            response_message = "Bạn cần đăng nhập để lưu lịch sử trò chuyện."
    else:
        response_message = "Không có tin nhắn nào được nhận."

    return jsonify(response=response_message)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(success=False, message="Thiếu thông tin tài khoản hoặc mật khẩu")

    user = db_service.find_user(username)  
    if user and check_password_hash(user['password'], password):
        session['username'] = username  
        session['session_id'] = str(ObjectId())  
        return jsonify(success=True, message="Đăng nhập thành công")
    else:
        return jsonify(success=False, message="Sai tài khoản hoặc mật khẩu")

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(success=False, message="Thiếu thông tin tài khoản hoặc mật khẩu")

    existing_user = db_service.find_user(username)  
    if existing_user:
        return jsonify(success=False, message="Tên tài khoản đã tồn tại")

    hashed_password = generate_password_hash(password)
    db_service.insert_user(username, hashed_password)  

    return jsonify(success=True, message="Đăng ký thành công")

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('session_id', None) 
    return jsonify(success=True, message="Đăng xuất thành công")

if __name__ == '__main__':
    app.run(debug=True)
