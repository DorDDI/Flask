from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.users.routes import users
    from app.movie_section.main.routes import movie_main
    from app.movie_section.posts.routes import movie_posts
    from app.menu.routes import menu
    from app.errors.handlers import errors
    from app.music_section.main.routes import music_main
    from app.music_section.posts.routes import music_posts

    app.register_blueprint(users)
    app.register_blueprint(movie_main)
    app.register_blueprint(movie_posts)
    app.register_blueprint(menu)
    app.register_blueprint(errors)
    app.register_blueprint(music_main)
    app.register_blueprint(music_posts)

    return app
