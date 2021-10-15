from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
import re
from . import db
# import request

auth = Blueprint('auth', __name__)


def check_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    else:
        return True

def check_password(password):
    len_password = len(password)

    if len_password > 25 or len_password < 3:
        return False
    else:
        return True

def check_name(name):
    len_name = len(name)

    if len_name < 1 or len_name > 45:
        return False
    else:
        return True


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    if not check_email(email):
        flash('Not valid email')
        return redirect(url_for('auth.signup'))
        
    if not check_name(name):
        flash('Not valid name')
        return redirect(url_for('auth.signup'))
    if not check_password(password):
        flash('Not valid password')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')

    if not check_email(email):
        flash('Not valid email')
        return redirect(url_for('auth.login'))
    if not check_password(password):
        flash('Not valid password')
        return redirect(url_for('auth.login'))

    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))
