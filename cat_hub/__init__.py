from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .my_config import Config
from flask_login import LoginManager
import os

db = SQLAlchemy()


class CurrentUserError:
    is_authenticated = False


def create_app(test_config=None):
    
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config is None:
        pass
    else:
        app.config.update(test_config)
        
    db.init_app(app)


    app.config['ABSOLUTE_UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'hub', 'user')

    if not os.path.exists(app.config['ABSOLUTE_UPLOAD_FOLDER']):
        os.makedirs(app.config['ABSOLUTE_UPLOAD_FOLDER'])

    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'])
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception as error:
            with open(app.config['LOG_FILE'], 'a+') as f:
                f.write(str(error))
            current_user = CurrentUserError()
            return current_user

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app._static_folder = 'static'

    from .photo_operation import photo_operation as photo_operation_blueprint
    app.register_blueprint(photo_operation_blueprint)

    return app
