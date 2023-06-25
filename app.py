from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, join_room, leave_room, emit, rooms
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
socketio = SocketIO(app)

names = ['Bou', 'Daa']
# List to store waiting users
waiting_users = []

# ex
@socketio.on('connect')
def handle_connect():

    user_id = request.sid
    print(f'User {user_id} connected')
    print(f'User {user_id} assigned rooms: {rooms(sid=user_id)}')

    if not waiting_users:
        waiting_users.append(user_id)
        room_name = f"{user_id}"
        join_room(room_name, sid=user_id)
        print(f'User {user_id} joining the room {room_name}')
        #join_room(f"room-{user_id}", sid=user_id)
        send('Waiting for a user...', room=user_id)
        print(f'User {user_id} created and joined the room {user_id}')
        print(f'User {user_id} assigned rooms: {rooms(sid=user_id)}')
        
        user_rooms = rooms(sid=user_id)
        if room_name in user_rooms:
            print(f"User {user_id} is IN {room_name}")
        else:
            print(f"User {user_id} is NOT IN {room_name}")
        
    else:
        waiting_user = waiting_users.pop()
        waiting_room = f"{waiting_user}"

        join_room(waiting_room, sid=user_id)
        join_room(waiting_room, sid=waiting_user)

        send('You are now connected to a creep', room=waiting_room)
        print(f'User {user_id} joined room {waiting_room}')
        print(f'User {user_id} assigned rooms: {rooms(sid=user_id)}')
#


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/peer_to_peer')
def peer_to_peer():
  return render_template('peer_to_peer.html')

# new
@socketio.on('join')
def on_join(data):

    room = request.sid
    join_room(room)
    socketio.emit('assign_name', room=room)

@socketio.on('send_message')
def send_msg(data):
    message = data['message']
    username = request.sid
    # Get the room the user is currently in
    user_rooms = rooms(sid=username)
    # Get the room the user is currently in
    room = [room for room in rooms(sid=username)][0]
    socketio.emit('chat', {'username': username, 'message': message}, room=room)



@socketio.on('message')
def handle_message(msg):
    user_id = request.sid
    room_name = next((room for room in rooms(sid=user_id) if room.startswith("room-")), None)
    print(f'User {user_id} attempted to send message "{msg}"')
    if room_name is not None:
        print(f'User {user_id} sent message "{msg}" in room {room_name}')
    else:
        print(f'User {user_id} not in room. Message not sent.')

if __name__ == '__main__':
      socketio.run(app)
