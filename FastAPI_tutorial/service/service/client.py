html = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WebSocket Chat</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-image: url('https://example.com/your-background-image.jpg'); /* Thay thế bằng URL ảnh của bạn */
                background-size: cover;
                background-position: center;
            }
            .chat-container {
                width: 1080px; /* Tăng độ rộng của khung chat */
                background-color: rgba(255, 255, 255, 0.8); /* Màu nền với độ trong suốt */
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            .chat-header {
                background-color: #007bff;
                color: #ffffff;
                padding: 10px;
                border-radius: 8px 8px 0 0;
                text-align: center;
            }
            .chat-messages {
                flex-grow: 1;
                padding: 15px;
                overflow-y: auto;
                border-bottom: 1px solid #f4f4f4;
            }
            .chat-messages ul {
                list-style-type: none;
                padding: 0;
                margin: 0;
            }
            .chat-messages li {
                margin-bottom: 10px;
                padding: 8px 10px;
                background-color: #e9e9e9;
                border-radius: 5px;
                max-width: 80%;
                word-wrap: break-word;
            }
            .chat-form {
                display: flex;
                padding: 10px;
                background-color: #f4f4f4;
                border-radius: 0 0 8px 8px;
            }
            .chat-form input[type="text"] {
                flex-grow: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-right: 10px;
            }
            .chat-form button {
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .chat-form button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <h2>API chat by Quan IT</h2>
            </div>
            <div class="chat-messages" id="chat-messages">
                <ul id="messages"></ul>
            </div>
            <form class="chat-form" action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" placeholder="Enter your message" autocomplete="off"/>
                <button type="submit">Send</button>
            </form>
        </div>
        <script>
            var ws;
            var maxMessages = 15; // Số lượng tin nhắn tối đa hiển thị trên màn hình

            function connectWebSocket() {
                ws = new WebSocket("ws://172.31.99.42:8000/chat_with_people");

                ws.onopen = function(event) {
                    console.log("WebSocket connection established.");
                };

                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);

                    // Giữ lại tối đa 15 tin nhắn trên giao diện
                    if (messages.children.length > maxMessages) {
                        messages.removeChild(messages.firstChild);
                    }

                    // Cuộn xuống dưới cùng khi có tin nhắn mới mà không làm mất tin nhắn cũ
                    var chatMessages = document.getElementById('chat-messages');
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                };

                ws.onclose = function(event) {
                    console.log("WebSocket connection closed:", event);
                    // Tự động kết nối lại sau 1 giây nếu kết nối bị đóng
                    setTimeout(function() {
                        console.log("Reconnecting WebSocket...");
                        connectWebSocket();
                    }, 1000);
                };

                ws.onerror = function(event) {
                    console.error("WebSocket error observed:", event);
                };
            }

            function sendMessage(event) {
                if (ws.readyState === WebSocket.OPEN) {
                    var messageText = document.getElementById("messageText").value;

                    if (messageText === "") {
                        alert("Please enter a message.");
                        return;
                    }

                    ws.send(messageText);
                    document.getElementById("messageText").value = '';
                } else {
                    console.error("WebSocket is not open. ReadyState: " + ws.readyState);
                }
                event.preventDefault();
            }

            // Khởi tạo kết nối WebSocket khi trang được tải
            window.onload = function() {
                connectWebSocket();
            };
        </script>
    </body>
</html>
"""