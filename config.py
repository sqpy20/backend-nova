from datetime import timedelta

class Config:
    SECRET_KEY = '0ccd2509577680dbc52d1582b56401550b986f09cfaa013da7fc'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '0ccderer47680dbc52d1582b56401550b986f09cfaa013da7fc'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=5)
    JWT_ERROR_MESSAGE_KEY = 'Token expired'
