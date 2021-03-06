from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index() -> str:
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile() -> str:
    return render_template('profile.html', name=current_user.name)


@main.route('/hello')
def for_test() -> str:
    return b'Hello!!!!'