from flask import Blueprint
from datetime import datetime
from flask import Flask, Response, render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message as ExternalMessage
from homepage import db
from homepage.messages.forms import NewMessageForm
from homepage.models import User, Note, Link, Message

messages = Blueprint('messages', __name__)

# I think I don't need this anymore, but not 100% sure
"""def coerce_recipient_username(recipient_data):
    x = recipient_data.split("'")
    return x[1]"""

@login_required
@messages.route('/view_messages')
def view_messages():
    message_list = []
    user = User.query.order_by(Message.time_sent.desc()).get(current_user.id)
    sent_messages = user.sent_messages
    for message in sent_messages:
        sender = current_user.username
        recipient = User.query.get(message.recipient_id).username
        message_list.append((message, sender, recipient))
    for message in Message.query.order_by(Message.time_sent.desc()).filter_by(recipient_id=current_user.id):
        message.unread = False
        db.session.commit()
        sender = User.query.get(message.sender_id).username
        recipient = current_user.username
        message_list.append((message, sender, recipient))

    sorted_message_list = sorted(
        message_list,
        key=lambda x: datetime.strptime(x[0].time_sent.strftime('%m/%d/%Y/%H'), '%m/%d/%Y/%H'), reverse=True
    )
    return render_template('view_messages.html', messages=sorted_message_list)

@messages.route('/new_message', methods=['GET', 'POST'])
@login_required
def new_message():
    possible_recipients = [(user.username, user.username) for user in User.query.all()]
    form = NewMessageForm(choices=possible_recipients)
    form.recipient.choices = possible_recipients
    if form.validate_on_submit():
        recipient_username = form.recipient.data
        recipient_id_number = User.query.filter_by(username=recipient_username).first().id
        message = Message(sender_id=current_user.id, subject=form.subject.data, 
                            body=form.body.data, sender=current_user, recipient_id=recipient_id_number)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("main.home"))
    return render_template("new_message.html", title="New Message", form=form, possible_recipients=possible_recipients)

@login_required
@messages.route('/messages/<int:message_id>/')
def view_message(message_id):
    message = Message.query.get_or_404(message_id)
    if current_user.id != message.recipient_id and current_user.id != message.sender_id:
        abort(403)
    sender = User.query.get(message.sender_id).username
    recipient = User.query.get(message.recipient_id).username

    return render_template('message.html', message=message, sender=sender, recipient=recipient)