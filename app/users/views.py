from app import app, db
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import logout_user, current_user, login_user
from oauth import OAuthSignIn
from models import *


users_blueprint = Blueprint("users", __name__, template_folder="templates") 


@users_blueprint.route('/index')
def index():
    return render_template('index.html')


@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.index'))


@users_blueprint.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('users.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@users_blueprint.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('users.index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    print social_id, username, email
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('users.index'))
    user = Users.query.filter_by(social_id=social_id).first()
    if not user:
        user = Users(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('users.index'))
    