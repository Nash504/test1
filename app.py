from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
socketio = SocketIO(app)

clients = {}

@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/index', methods=['GET'])
def index():
    username = request.args.get('username')
    if username:
        session['username'] = username
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@socketio.on('connect')
def handle_connect():
    print("A user connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("A user disconnected")
    username = clients.get(request.sid)
    if username:
        emit('message', f"{username} has left the chat", broadcast=True)
        del clients[request.sid]

@socketio.on('set_username')
def handle_set_username(username):
    clients[request.sid] = username
    emit('message', f"{username} has joined the chat", broadcast=True)

@socketio.on('send_message')
def handle_send_message(msg):
    username = clients.get(request.sid, "Anonymous")
    emit('message', f"{username}: {msg}", broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)

