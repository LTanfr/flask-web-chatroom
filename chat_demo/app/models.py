import hashlib
from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email_hash = db.Column(db.String(128))
    messages = db.relationship('Message', back_populates='author', cascade='all')

    # 调试时打印用户实例
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.generate_email_hash()

    def generate_email_hash(self):
        if self.email is not None and self.email_hash is None:
            # hashlib.md5摘要算法（哈希算法）
            self.email_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    @property
    def gravatar(self):
        return 'https://www.gravatar.com/avatar/%s?d=wavatar' % self.email_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='messages')

    # 调试时打印用户实例
    def __repr__(self):
        return '<Message {}>'.format(self.author.username, self.body)