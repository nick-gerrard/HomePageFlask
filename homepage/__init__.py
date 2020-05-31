from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from homepage.config import Config
from flask_migrate import Migrate


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
migrate =  Migrate()

mail = Mail()





def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from homepage.users.routes import users
    from homepage.main.routes import main
    from homepage.notes.routes import notes
    from homepage.data.routes import data
    from homepage.messages.routes import messages
    from homepage.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(notes)
    app.register_blueprint(data)
    app.register_blueprint(messages)
    app.register_blueprint(errors)

    return app