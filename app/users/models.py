import os
import datetime
from app import db, bcrypt 
from sqlalchemy import DDL, event
from sqlalchemy.ext.hybrid import hybrid_property


class UsersProfile(db.Model):
    """ Top level profile of site when user registers either by email or by social 
    info from that registraition process is stored here.  
    Also any changes to profile from /profile are saved here and show on site.  
    """
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

    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

# Define Role model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define UserRoles model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users_profile.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


class UsersRegister(db.Model):
    """ User model for users to register using email address """

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
    """ Model to have users sign up for site using thier own social media accounts """

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
    """ Model to name the social media accounts by id and name. ie Facebook, Github  """

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
event.listen(
    Role.__table__, 'after_create',
    DDL(
        """ INSERT INTO role (id,name) VALUES(1, 'userbasic'), (2,'editor'), (3, 'super'), (4, 'admin');""")
)