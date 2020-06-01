#!/home/nickg/homepageflask/venv/bin/python

from homepage import db, create_app
from homepage.models import *

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


