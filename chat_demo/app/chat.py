from app import socketio, db
from flask_socketio import emit
from app.models import Message, User
from flask import render_template
from flask_login import current_user

online_users = []


@socketio.on('new message')
def handle_new_message(msg):
    auth = User.query.filter_by(username=msg['username']).first()
    message = Message(author=auth, body=msg['input'])
    db.session.add(message)
    db.session.commit()
    emit('new message',
         {
             'message_x': render_template("message_x.html", message=message),
             'message_y': render_template("message_y.html", message=message),
             'username': msg['username']
         },
         broadcast=True)


@socketio.on('connect')
def connect():
    global online_users
    if current_user.is_authenticated and current_user.id not in online_users:
        online_users.append(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)


@socketio.on('disconnect')
def disconnect():
    global online_users
    if current_user.is_authenticated and current_user.id in online_users:
        online_users.remove(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)
