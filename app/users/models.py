import os
import datetime
from app import db, bcrypt 
from sqlalchemy import DDL, event
from sqlalchemy.ext.hybrid import hybrid_property


# class Users(UserMixin, db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     social_id = db.Column(db.String(64), nullable=False, unique=True)
#     nickname = db.Column(db.String(64), nullable=False)
#     email = db.Column(db.String(64), nullable=True)


class UsersProfile(db.Model):
    __tablename__ = "users_profile"
    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.String(50))
    avatar = db.Column(db.String(), default="user.jpg")
    email = db.Column(db.String(255))#, unique=True
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    last_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(45))
    current_login_at = db.Column(db.DateTime)
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer, default=0) 
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class UsersRegister(db.Model):
    __tablename__ = 'users_register'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True) 
    email = db.Column(db.String(255), nullable=False, unique=True)
    _password = db.Column(db.String(255), nullable=False) #hybrid column
    confirmed = db.Column(db.Boolean(), default=False) 
    confirmed_at = db.Column(db.DateTime)
    users_id = db.Column(db.Integer, db.ForeignKey('users_profile.id', ondelete='CASCADE'), index=True)
    users = db.relationship("UsersProfile", foreign_keys=users_id)

    @hybrid_property 
    def password(self):
        return self._password 

    @password.setter 
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

class SocialLogin(db.Model):
    __tablename__ = "social_login"
    id = db.Column(db.Integer, primary_key=True)

    social_login_id = db.Column(db.String(64), nullable=False, unique=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(255))
    avatar = db.Column(db.String(255))

    provider_name_id = db.Column(db.Integer, db.ForeignKey('provider_name.id'))
    provider_name = db.relationship('ProviderName', foreign_keys=provider_name_id)

    users_id = db.Column(db.Integer, db.ForeignKey('users_profile.id', ondelete='CASCADE'), index=True)
    users = db.relationship("UsersProfile", foreign_keys=users_id)

class ProviderName(db.Model):
    __tablename__ = "provider_name"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class TodoItem(db.Model):
    __tablename__="todo_item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    is_done = db.Column(db.Boolean, default=False)
    creation_date = db.Column(db.Date, default=datetime.datetime.utcnow())
    deadline_date = db.Column(db.Date)
    users_id = db.Column(db.Integer, db.ForeignKey('users_profile.id', ondelete='CASCADE'), index=True)
    users = db.relationship("UsersProfile", foreign_keys=users_id) 

event.listen(
    ProviderName.__table__, 'after_create',
    DDL(
        """ INSERT INTO provider_name (id,name) VALUES(1,'facebook'),(2, 'google'),(3, 'github'), (4, 'linkedin'), (5, 'twitter'), (6, 'foursquare'), (7, 'reddit'); """)
)
