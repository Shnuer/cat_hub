from flask_login import UserMixin

from sqlalchemy.sql import func
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    liked = db.relationship(
        'PhotoLike',
        foreign_keys='PhotoLike.user_id',
        backref='user',
        lazy='dynamic')

    def like_photo(self, photo):
        if not self.has_liked_photo(photo):
            like = PhotoLike(user_id=self.id, photo_id=photo.id)
            db.session.add(like)

    def unlike_photo(self, photo):
        if self.has_liked_photo(photo):
            PhotoLike.query.filter_by(
                user_id=self.id,
                photo_id=photo.id).delete()

    def has_liked_photo(self, photo):
        return PhotoLike.query.filter(
            PhotoLike.user_id == self.id,
            PhotoLike.photo_id == photo.id).count() > 0


class UserPhoto(db.Model):
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(1000))
    upload_time = db.Column(db.DateTime(timezone=True), default=func.now())

    likes = db.relationship('PhotoLike', backref='user_photo', lazy='dynamic')



class PhotoComment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo = db.Column(db.Integer, db.ForeignKey('user_photo.id'))
    text = db.Column(db.String(1000))  
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())



class PhotoLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo_id = db.Column(db.Integer, db.ForeignKey('user_photo.id'))
