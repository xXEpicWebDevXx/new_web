from email.policy import default
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func




class Image(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    suffix = db.Column(db.String(20))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    privs = db.Column(db.Integer)
    email = db.Column(db.String(150),unique = True)
    password = db.Column(db.String(150))
    nick = db.Column(db.String(150))
    imgs = db.relationship('Image')