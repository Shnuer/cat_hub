from flask_login import UserMixin
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class UserPhoto(db.Model):
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo_id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(1000))
    upload_time = db.Column(db.DateTime(timezone=True), default=func.now())
    # add original_name
    # add column with likes


class PhotoComment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo = db.Column(db.Integer, db.ForeignKey('user_photo.photo_id'))
    text = db.Column(db.String(1000))  # add text column
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    # add datetime column

class PhotoLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo_id = db.Column(db.Integer, db.ForeignKey('user_photo.photo_id'))
