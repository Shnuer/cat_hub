from flask import Blueprint, render_template, request, redirect, url_for, current_app
from . import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import uuid
import os
from .models import User, UserPhoto
from sqlalchemy import desc


main = Blueprint('main', __name__)


def generate_new_file_name(file_name: str) -> str:
    new_name = str(uuid.uuid4()) + '.' + file_name.split('.')[-1]
    return new_name


def generate_path(path_name: str) -> None:
    if not os.path.exists(path_name):
        os.makedirs()


def check_directory(upload_dir: str, user_name: str) -> str:
    user_path = os.path.join(upload_dir, user_name)
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    return user_path


@main.route('/')
def index() -> str:
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile() -> str:
    return render_template('profile.html', name=current_user.name)


@main.route('/upload_photo')
@login_required
def photo_upload_page():
    return render_template('photo_upload.html')


@main.route('/user_album', methods=['POST'])
@login_required
def photo_upload():
    uploaded_file = request.files['file']

    if uploaded_file.filename != '': # add checking for format like .png .jpeg and another
        new_name = generate_new_file_name(uploaded_file.filename)

        absolute_user_directory = check_directory(current_app.config['ABSOLUTE_UPLOAD_FOLDER'], current_user.name)
        absolute_result_directory = os.path.join(absolute_user_directory, new_name)

        local_user_directory = os.path.join(current_app.config['LOCAL_UPLOAD_FOLDER'], current_user.name)
        local_result_directory = os.path.join(local_user_directory, new_name)

        uploaded_file.save(absolute_result_directory)

        user = User.query.filter_by(name=current_user.name).first()
        photo = UserPhoto(owner=user.id, path=local_result_directory)

        db.session.add(photo)
        db.session.commit()

    return redirect(url_for('main.show_photo'))


@main.route('/user_album')
@login_required
def show_photo():
    user = User.query.filter_by(name=current_user.name).first()
    all_image = (UserPhoto.query.filter_by(owner=user.id).all())

    return render_template('album.html', all_img=all_image)


@main.route('/news')
@login_required
def show_all_photo():
    all_image = UserPhoto.query.order_by(desc(UserPhoto.upload_time)).all()
    return render_template('news.html', all_img=all_image, show=True)

