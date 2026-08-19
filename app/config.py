import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    FLASK_RUN_PORT = os.environ.get('FLASK_RUN_PORT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Production platforms may still provide the legacy `postgres://` scheme,
    # while local development and CI should work without a DATABASE_URL.
    _database_url = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
    SQLALCHEMY_DATABASE_URI = _database_url.replace(
        'postgres://', 'postgresql://', 1
    )

    SQLALCHEMY_ECHO = True
