from app import app, db
from app.chat import online_users
from flask import render_template, flash, redirect, url_for, request, current_app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Message


@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat_with_list'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误。')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('chat_with_list'))
    return render_template('login.html', title='登 录', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/chat_with_list', methods=['POST', 'GET'])
@login_required
def chat_with_list():
    return render_template('chat_with_list.html')


# @app.route('/chat', methods=['POST', 'GET'])
# @login_required
# def chat():
#     return render_template('chat.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注 册', form=form)


@app.route('/messages')
def get_messages():
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.order_by(Message.timestamp.desc()).paginate(
        page, per_page=current_app.config['MESSAGE_PER_PAGE'])
    messages = pagination.items
    return render_template('messages.html', messages=messages[::-1])


@app.route('/users')
def get_users():
    return render_template('users.html', users=online_users)
