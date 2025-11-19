import os

class Config:
    SECRET_KEY = 'dev-secret-key'     # Temporary Flask secret. todo; Set by env variable or config.yml.

    DB_PATH = '/app/message.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'

    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
