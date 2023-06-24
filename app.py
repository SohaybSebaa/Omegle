from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, join_room, leave_room, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
socketio = SocketIO(app)

names = ['Bou', 'Daa']
# List to store waiting users
waiting_users = []


@socketio.on('connect')
def handle_connect():

    user_id = request.sid
    
    # Check if there is another waiting user
    if waiting_users:
        # Get the first waiting user
        partner_id = waiting_users.pop()
        room = f"room-{user_id}-{partner_id}"
        
        # Get the second waiting user
        join_room(room, sid=user_id)
        join_room(room, sid=partner_id)

        send('You are now connected to a creep', room=room)
        
    else:
        waiting_users.append(user_id)
        send('Waiting for a user...', room=user_id)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/peer_to_peer')
def peer_to_peer():
  return render_template('peer_to_peer.html')

# new
@socketio.on('join')
def on_join(data):
    username = random.choice(names)
    names.remove(username)
    room = request.sid
    join_room(room)
    socketio.emit('assign_name', {'username': username}, room=room)

@socketio.on('send_message')
def send_msg(data):
    message = data['message']
    username = request.sid
    socketio.emit('chat', {'username': username, 'message': message})


if __name__ == '__main__':
      socketio.run(app)
