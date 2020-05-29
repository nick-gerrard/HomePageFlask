import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from homepage import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    notes = db.relationship('Note', backref='author', lazy=True)
    links = db.relationship('Link', backref='author', lazy=True)
    sent_messages = db.relationship('Message', backref="sender", lazy=True)

    def get_reset_token(self, expieres_sec=9000):
        s = Serializer(current_app.config['SECRET_KEY'], expieres_sec)
        return s.dumps({"user_id": self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Note('{self.title}', '{self.date_posted}'')"


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Link('{self.title}', '{self.address}'')"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(120), nullable=False, default="Subject")
    body = db.Column(db.Text, nullable=False)
    time_sent = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    unread = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"""Message(Sender: {User.query.get(self.sender_id).username}
Recipient: {User.query.get(self.sender_id).username}
Subject: {self.subject}
Body: {self.body}
"""




