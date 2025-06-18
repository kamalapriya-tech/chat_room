from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, join_room
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'priya'
socketio = SocketIO(app)

# --- Database Connection ---
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="hello",
        database="chat_app"
    )

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = generate_password_hash(request.form['password'])

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return redirect(url_for('index'))
    except:
        return "Username already exists"
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user[0], password):
        session['username'] = username
        return redirect(url_for('join_room_page'))
    return "Invalid credentials"

@app.route('/join', methods=['GET', 'POST'])
def join_room_page():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        room = request.form['room']
        session['room'] = room
        return redirect(url_for('chat'))
    return render_template('join.html')

@app.route('/chat')
def chat():
    if 'username' not in session or 'room' not in session:
        return redirect(url_for('index'))

    # Load past messages in this room
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sender, content FROM messages WHERE room = %s ORDER BY timestamp", (session['room'],))
    messages = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('chat.html', username=session['username'], room=session['room'], messages=messages)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- Socket Events ---
@socketio.on('join')
def handle_join(room):
    join_room(room)
    send(f"{session['username']} has joined the room.", to=room)

@socketio.on('message')
def handle_message(data):
    msg = data['msg']
    room = data['room']
    sender = session.get('username', 'Anonymous')

    # Save to DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender, content, room) VALUES (%s, %s, %s)", (sender, msg, room))
    conn.commit()
    cursor.close()
    conn.close()

    send(f"{sender}: {msg}", to=room)

# --- Main ---
if __name__ == '__main__':
    socketio.run(app, debug=True)
