import pytest
from cat_hub.models import User
from flask_login import current_user


def test_register(client, app):
    assert client.get('/signup').status_code == 200
    response = client.post(
        '/signup',
        data = {'email': 'some@mail.ro', 'password': '1231324', 'name': 'valid_name'}
        )
    
    assert 'http://localhost/login' == response.headers['Location']
    with app.app_context():
        assert User.query.filter_by(email='some@mail.ro').first() is not None
        

@pytest.mark.parametrize(('email', 'username', 'password', 'message'),(
    ('', '', '', b'Not valid email.'),
    ('some@mail.ro', '', '', b'Not valid name.'),
    ('some@mail.ro', 'valid_name', '', b'Not valid password.'),
))
def test_register_validate_input(client, email, username, password, message):
    response = client.post(
        '/signup',
        data={'name': username, 'email': email, 'password': password},
        follow_redirects=True
        )

    assert message in response.data


def test_login(client, auth):
    
    assert client.get('/login').status_code == 200
    
    response = auth.login()

    assert response.headers['Location'] == 'http://localhost/profile'

    with client:
        client.get('/')
        assert current_user.name == 'test'
        assert current_user.id == 1


def test_logout(client, auth):

    auth.login()

    with client:
        auth.logout()
        assert current_user.get_id() == None
