from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from . import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import uuid
import os
from .models import User, UserPhoto, PhotoComment
from sqlalchemy import desc, delete


photo_operation = Blueprint('photo_operation', __name__)


def handle_exception(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as error:
            return catch_error(error)

    return wrapper


def catch_error(error):
    log_file = current_app.config['LOG_FILE']
    with open(log_file, 'a+') as f:
        f.write(str(error))
    return redirect(url_for('photo_operation.show_error'))


def allowed_file(valid_format, file_name):
    if file_name.rsplit('.', 1)[1] in valid_format:
        return True
    return False


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


def save_file(uploaded_file):
    new_name = generate_new_file_name(uploaded_file.filename)
    secure_name = secure_filename(new_name)

    absolute_user_directory = check_directory(current_app.config['ABSOLUTE_UPLOAD_FOLDER'], current_user.name)
    absolute_result_directory = os.path.join(absolute_user_directory, secure_name)

    local_user_directory = os.path.join(current_app.config['LOCAL_UPLOAD_FOLDER'], current_user.name)
    local_result_directory = os.path.join(local_user_directory, secure_name)

    uploaded_file.save(absolute_result_directory)
    return local_result_directory


@photo_operation.route('/error')
def show_error():
    return render_template('error_page.html')


@handle_exception
@photo_operation.route('/user_album', methods=['POST'])
@login_required
def photo_upload():
    uploaded_file = request.files['file']

    if allowed_file(current_app.config['VALID_FORMATS'], secure_filename(uploaded_file.filename)):

        local_result_directory = save_file(uploaded_file)
        user = User.query.filter_by(name=current_user.name).first()
        photo = UserPhoto(owner=user.id, path=local_result_directory)

        db.session.add(photo)
        db.session.commit()
    else:
        flash('Not valid file format')

    return redirect(url_for('photo_operation.show_photo'))


@handle_exception
@photo_operation.route('/user_album')
@login_required
def show_photo():
    user = User.query.filter_by(name=current_user.name).first()
    all_image = (UserPhoto.query.filter_by(owner=user.id).all())

    return render_template('album.html', all_img=all_image)


@handle_exception
@photo_operation.route('/news')
@login_required
def show_all_photo():
    comments = PhotoComment.query.order_by(desc(PhotoComment.created_date)).all()
    all_image = UserPhoto.query.order_by(desc(UserPhoto.upload_time)).all()
    all_user = User.query.order_by().all()

    return render_template('news.html', all_img=all_image, all_comments=comments, all_user=all_user)


@handle_exception
@photo_operation.route('/like/<int:photo_id>/<action>')
@login_required
def like_action(photo_id, action):

    photo = UserPhoto.query.filter_by(id=photo_id).first_or_404()

    if action == 'like':
        current_user.like_photo(photo)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_photo(photo)
        db.session.commit()

    return redirect(request.referrer)


@handle_exception
@photo_operation.route('/add_comment/<int:photo_id>',  methods=['POST'])
@login_required
def add_comment(photo_id):

    text = request.form.get('comment')
    if text:
        user = User.query.filter_by(name=current_user.name).first()
        photo = UserPhoto.query.filter_by(id=photo_id).first()
        comment = PhotoComment(user=user.id, photo=photo.id, text=str(text))
        db.session.add(comment)
        db.session.commit()

    return redirect(request.referrer)


@handle_exception
@photo_operation.route('/delete/<photo_id>', methods=['POST'])
@login_required
def delete_photo(photo_id):

    user = User.query.filter_by(name=current_user.name).first_or_404()
    photo = UserPhoto.query.filter_by(id=photo_id).first_or_404()
    if not user.id == photo.owner:
        flash('You cant remove this photo')
        return redirect(request.referrer)
    else:
        exists = db.session.query(PhotoComment.comment_id).filter_by(photo=photo_id).first() is not None

        if exists:
            sql1 = delete(PhotoComment).where(PhotoComment.photo.in_([photo_id]))
            db.session.execute(sql1)

        db.session.delete(photo)
        db.session.commit()
        flash('You delete your photo')
        return redirect(request.referrer)

