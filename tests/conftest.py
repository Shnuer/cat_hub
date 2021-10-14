import pytest
from cat_hub import db, create_app
from flask_sqlalchemy import SessionBase
from cat_hub.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user

# db.create_all(app=create_app())
@pytest.fixture
def app():
    app = create_app({'TESTING': True,
                      'EMAIL': 'Keks',
                      'PASSWORD': 'Keks',
                      'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://test_cat_hub:4321@localhost/test_cat_hub_db'})

    with app.app_context():
        db.init_app(app)
        # db.create_scoped_session()
        db.create_all()
        password=generate_password_hash('test', method='sha256')
        test_user = User(email='test@test.test', password=password, name='test')

        db.session.add(test_user)
        db.session.commit()
    
    yield app

    with app.app_context():
        db.drop_all()




@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client) -> None:
        self._client = client

    def login(self, email='test@test.test', password='test'):
        
        return self._client.post(
            '/login',
            data={'email': email, 'password': password}
        )

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)

    # ,
    #     follow_redirects=True