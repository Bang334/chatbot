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

// Xử lý lưu lịch sử trò chuyện
document.querySelector('.SaveHistory').addEventListener('click', async () => {
  const response = await fetch('/api/history');
  const data = await response.json();

  const chatBox = document.getElementById('chat-box');
  chatBox.innerHTML = '';  // Xóa nội dung hiện tại trong khung chat

  // Hiển thị từng bản ghi trong lịch sử
  data.history.forEach(record => {
      const userMessageDiv = document.createElement('div');
      userMessageDiv.className = 'chat chat-end';
      userMessageDiv.innerHTML = `<div class="py-3 px-5 rounded-full bg-mes_bg text-mes_te">${record.message}</div>`;
      chatBox.appendChild(userMessageDiv);
      const botResponseDiv = document.createElement('div');
      botResponseDiv.className = 'chat chat-start';
      botResponseDiv.innerHTML = `<div class="py-3 px-5 rounded-full bg-mes_bg text-mes_te">${record.response}</div>`;
      chatBox.appendChild(botResponseDiv);
      const timeDiv = document.createElement('div');
      timeDiv.className = 'chat-time text-gray-400 text-sm'; 
      const timestamp = new Date(record.timestamp); 
      timeDiv.innerHTML = `<div>${timestamp.toLocaleString()}</div>`; 
      chatBox.appendChild(timeDiv);
  });
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
