from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .my_config import Config
from flask_login import LoginManager
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.config['ABSOLUTE_UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'hub', 'user')
    app.config['LOCAL_UPLOAD_FOLDER'] = os.path.join('static', 'hub', 'user')
    if not os.path.exists(app.config['ABSOLUTE_UPLOAD_FOLDER']):
        os.makedirs(app.config['ABSOLUTE_UPLOAD_FOLDER'])
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


