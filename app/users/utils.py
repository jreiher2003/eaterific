from app import app, mail 
from flask_mail import Message
from flask_login import current_user
from flask import flash, redirect, url_for
from .models import UsersProfile

def get_current_user_role():
    user_register = UsersProfile.query.filter_by(id=current_user.id).first() 
    l = []
    for name in user_register.roles:
        l.append(name.name)
    return l 

from functools import wraps
def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            role_list = get_current_user_role()
            if not any(role in role_list for role in roles):
                flash("you are not permited to visit this page")
                return redirect(url_for("rest.index"))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def send_email(to, subject, template):
    msg = Message(subject, recipients=[to], html=template, sender=app.config["MAIL_DEFAULT_SENDER"])
    return mail.send(msg) 

