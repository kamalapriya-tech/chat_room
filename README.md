


markdown
 💬 Real-Time Chat App with Rooms

A simple real-time chat application built using **Flask**, **Socket.IO**, and **MySQL** with room support.

 🚀 Features

- 🔐 User Registration & Login
- 🧑‍🤝‍🧑 Join a Chat Room (`join.html`)
- 💬 Real-Time Messaging using Socket.IO
- 🗃️ Messages stored in MySQL
- 🎨 Simple, stylish UI
 🗂️ Files

-app.p– Flask backend with Socket.IO and MySQL
- templates/index.html – Login/Register
- templates/join.html – Select or create a room
- templates/chat.html – Chat interface
- static/style.css – Optional CSS styling

## 🛠️ Setup

1. Create MySQL DB:

sql
CREATE DATABASE chat_app;
USE chat_app;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) UNIQUE,
  password VARCHAR(255)
);

CREATE TABLE messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sender VARCHAR(100),
  content TEXT,
  room VARCHAR(100),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


2. Install requirements:

bash
pip install flask flask-socketio mysql-connector-python werkzeug


3. Run app:

bash
python app.py


Visit "http://localhost:5000".

✅ Task Completed

✔️ Includes user login/register
✔️ Supports room-based real-time messaging
✔️ Messages stored in MySQL
✔️ Frontend styled with background and layout
✔️ Includes separate `join.html` for room entry



