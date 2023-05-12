import datetime
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin
import jwt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),  nullable=False, default= 'default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    music_posts = db.relationship('MusicPost', backref='author', lazy=True)
    movie_watchlist = db.relationship('MovieWatchlist', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        reset_token = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expires_sec)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return None
        return User.query.get(user_id['user_id'])

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class MusicPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class MovieWatchlist(db.Model):
    id = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    poster = db.Column(db.String(200), nullable=False)
    type_watch = db.Column(db.String(10), nullable=False)
    duration = db.Column(db.String(10), nullable=True)
    rate = db.Column(db.String(10), nullable=True)
    actors = db.Column(db.String(100), nullable=False)
    date_year = db.Column(db.String(10), nullable=False)
    content_rate = db.Column(db.String(10), nullable=False)
    genre = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    watch_id_number = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
