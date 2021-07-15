#!/home/nickg/homepageflask/venv/bin/python

from homepage import db, create_app, bcrypt
from homepage.models import *


def change_user_password(user, password):
    check = input(f"Are you sure you want to change {user.username}'s password to {password}? ")
    if check == "YES":
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        print(f"Success! {user.username}'s password has been updated")
    else:
        print("Aborting password change")

#Function to add link to user
def add_link(title, url, user):
    check = input(f"""Is this the link you want to add? Title: {title},
            URL: {url},
            user = {user.username}?
            Type Y to continue. """)
    if check == "Y":
        link = Link(title=title, address=url, user_id=user.id)
        db.session.add(link)
        db.session.commit()
        print(f"Success! {title} has been added to {user.username}'s homepage!")
    else:
        print("Failure. Aborting...")
# Pushing the context to be able to query the database:\
app = create_app()
app.app_context().push()

users = User.query.all()
notes = Note.query.all()
links = Link.query.all()
messages = Message.query.all()

print("Welcome to your database Nick!")
try:
    print(f"""\n
Total Users: {len(users)}
Total Notes: {len(notes)}
Total Links: {len(links)}
Total Messages: {len(messages)}
""")
except:
    print("Unable to pull database information. Please troubleshoot.")


