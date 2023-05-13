import os
from movies import Movie


class Config:
    SECRET_KEY = 'e05201e52103ae9e0b478dc038802df6'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    SECTION = 0
    RES = ''
    MOVIE = Movie()
    #SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    #SPOTIFY_CLIENT_SECRETS = os.environ.get('SPOTIFY_CLIENT_SECRETS')
