import os


class Config:
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'some-thing_important'
    FLASK_SECRET = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://secret_user:VerySecretPassword@localhost/cat_hub_db'
    INSTANCE_RELATIVE_CONFIG = True
    LOCAL_UPLOAD_FOLDER = os.path.join('static', 'hub', 'user')
    VALID_FORMATS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    LOG_DIR = os.path.join('static', 'log')
    LOG_FILE = os.path.join(LOG_DIR, 'error.log')


