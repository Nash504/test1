from flask import Flask, render_template,request
from flask_socketio import SocketIO, emit
app = Flask(__name__)
socketio = SocketIO(app)

clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("A user connected")

@socketio.on('disconnect') # browser is closed
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
