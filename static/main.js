let isLoggedIn = false; // Khai báo biến trạng thái đăng nhập

function SendMessage() {
  const messageInput = document.getElementById("user-message");
  if (messageInput.value == "") {
    return;
  }
  const chatBox = document.getElementById("chat-box");
  const userMessage = messageInput.value;
  chatBox.innerHTML += `<div class="chat chat-end"><div class="py-3 px-5 rounded-lg bg-neutral ml-10"> ${userMessage} </div></div>`;
  messageInput.value = "";

  fetch("/api/message", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userMessage }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Hiển thị phản hồi của server
      chatBox.innerHTML += `<div class="chat chat-start">
          <div class="py-3 px-5 rounded-lg bg-neutral mr-10"> ${data.response} </div></div>`;
      chatBox.scrollTop = chatBox.scrollHeight; // Tự động cuộn xuống cuối
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

document.getElementById("send-btn").addEventListener("click", () => {
  SendMessage();
});

document.getElementById("user-message").addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    SendMessage();
  }
});

window.onload = function () {
  document.getElementById("user-message").focus();
}

document.querySelector('.SaveHistory').addEventListener('click', async () => {
  try {
      const response = await fetch('/api/history');
      const data = await response.json();

      const chatBox = document.getElementById('chat-box');
      chatBox.innerHTML = '';  
      if (data.history.length === 0) {
        alert("Lịch sử trò chuyện rỗng.");
        return; 
      }
      console.log(data)
      data.history.forEach(session => {
          // const sessionHeader = document.createElement('h3');
          // sessionHeader.textContent = `Session ID: ${session.session_id}`;
          // chatBox.appendChild(sessionHeader);

          const displayedMessages = new Set();

          session.conversation.forEach(record => {
              const messageKey = `${record.role}-${record.parts}`;
              if (!displayedMessages.has(messageKey)) {
                  displayedMessages.add(messageKey);
                  const messageDiv = document.createElement('div');
                  messageDiv.className = record.role === 'user' ? 'chat chat-end' : 'chat chat-start';
                  messageDiv.innerHTML = `<div class="py-3 px-5 rounded-full bg-mes_bg text-mes_te">${record.parts}</div>`;
                  chatBox.appendChild(messageDiv);
              }
          });
          const timeDiv = document.createElement('div');
          timeDiv.className = 'chat-time text-gray-400 text-sm';
          const timestamp = new Date(); 
          timeDiv.innerHTML = `<div>${timestamp.toLocaleString()}</div>`;
          chatBox.appendChild(timeDiv);

          const divider = document.createElement('hr');
          divider.className = 'session-divider'; // Thêm class để định dạng nếu cần
          chatBox.appendChild(divider);
      });
  } catch (error) {
      console.error('Error fetching chat history:', error);
  }
});


// Xử lý nút tài khoản
document.getElementById("account-btn").addEventListener("click", () => {
  document.getElementById("account-modal").classList.remove("hidden");
});

document.getElementById("close-modal").addEventListener("click", () => {
  document.getElementById("account-modal").classList.add("hidden");
});

// Xử lý đăng nhập
document.getElementById("login-btn").addEventListener("click", () => {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  fetch("/api/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message);
      if (data.success) {
        isLoggedIn = true; 
        document.getElementById("account-modal").classList.add("hidden");
        document.getElementById("logout-btn").classList.remove("hidden"); 
        document.getElementById("login-btn").classList.add("hidden"); 
        document.getElementById("account-btn").classList.add("hidden");
        document.getElementById("login-username").value = '';  
        document.getElementById("login-password").value = '';  
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});


// Xử lý đăng ký
document.getElementById("register-btn").addEventListener("click", () => {
  const username = document.getElementById("register-username").value;
  const password = document.getElementById("register-password").value;

  fetch("/api/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data); 
      alert(data.message);
      if (data.success) {
        document.getElementById("account-modal").classList.add("hidden");
        document.getElementById("register-username").value = '';  
        document.getElementById("register-password").value = ''; 
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

// Xử lý đăng xuất
document.getElementById("logout-btn").addEventListener("click", () => {
  fetch("/api/logout", { method: "POST" }) 
    .then((response) => response.json()) 
    .then((data) => {
      alert(data.message); 
      if (data.success) {
        isLoggedIn = false; 
        document.getElementById("logout-btn").classList.add("hidden"); 
        document.getElementById("login-btn").classList.remove("hidden"); 
        window.location.reload();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
