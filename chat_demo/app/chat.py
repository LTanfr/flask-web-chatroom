from app import socketio, db
from flask_socketio import emit
from app.models import Message, User
from flask import render_template
from flask_login import current_user,logout_user

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


@socketio.on('user in')
def user_in(data):
    global online_users
    user = User.query.filter_by(username=data).first()
    if user not in online_users:
        online_users.append(user)
        emit('online users',
             {'users_html': render_template('users.html', users=online_users)},
             broadcast=True)


@socketio.on('user leave')
def user_leave(data):
    print(111111111111111111111)
    global online_users
    user = User.query.filter_by(username=data).first()
    if user in online_users:
        online_users.remove(user)
        emit('online users',
             {'users_html': render_template('users.html', users=online_users)},
             broadcast=True)


# @socketio.on('connect')
# def connect():
#     global online_users
#     if current_user.is_authenticated and current_user not in online_users:
#         online_users.append(current_user)
#         for user in online_users:
#             print(user.id, user.username)
#         emit('online users',
#              {'users_html': render_template('users.html', users=online_users)},
#              broadcast=True)


# @socketio.on('disconnect')
# def disconnect():
#     logout_user()
#     global online_users
#     print("3333333333333333333333333333")
#     if current_user.is_authenticated and current_user in online_users:
#         print("44444444444444444444444444444444")
#         online_users.remove(current_user)
#         emit('online users',
#              {'users_html': render_template('users.html', users=online_users)},
#              broadcast=True)
