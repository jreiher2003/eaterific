import datetime
from app import app, db
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import logout_user, current_user, login_user
from oauth import OAuthSignIn
from models import *
from .forms import * 


users_blueprint = Blueprint("users", __name__, template_folder="templates") 


@users_blueprint.route('/index')
def index():
    return render_template('index.html')

@users_blueprint.route("/login/", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_register = UsersRegister.query.filter_by(email=form.email.data).first() 
        if user_register is not None and bcrypt.check_password_hash(user_register.password, form.password.data):
            users = UsersProfile.query.filter_by(id=user_register.users_id).first()
            remember = form.remember.data
            users.login_count += 1
            users.last_login_ip = users.current_login_ip
            users.last_login_at = users.current_login_at
            users.current_login_ip = "10.0.0.1"
            users.current_login_at = datetime.datetime.now()
            print users, users.screen_name, users.id
            db.session.add(users)
            db.session.commit()
    
            login_user(users,remember)
            return redirect(url_for("users.index"))
        else:
            flash("<strong>Invalid Credentials.</strong> Please try again.", "danger")
            return redirect(url_for("users.login"))
    return render_template(
        "login.html",
        form=form
        )

@users_blueprint.route("/register/", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        users = UsersProfile(
            screen_name=form.username.data,
            email=form.email.data,
            login_count = 1,
            current_login_ip = "10.0.0.0",
            current_login_at = datetime.datetime.now(),
            )
        db.session.add(users)
        db.session.commit()
        user_register = UsersRegister(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data,
            users_id = users.id 
            )
        db.session.add(user_register)
        db.session.commit()
        login_user(users,True)
        flash("Welcome <strong>%s</strong> to Menu App. Please go to your inbox and confirm your email." % (user_register.username), "success")
        return redirect(url_for("users.index"))
    return render_template("register.html",form=form)


@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.index'))

@users_blueprint.route("/forgot-password")
def forgot_password():
    return "forgot password"


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
    social_login = SocialLogin.query.filter_by(social_login_id=social_id).first()
    # print social_login.id, social_login.users_id
    if social_login:
        print "if social"
        users = UsersProfile.query.filter_by(id=social_login.users_id).one_or_none()
        users.login_count += 1
        users.last_login_ip = users.current_login_ip
        users.last_login_at = users.current_login_at
        users.current_login_ip = "10.0.0.1"
        users.current_login_at = datetime.datetime.now()
        db.session.add(users)
        db.session.commit()
        login_user(users, True)
    if not social_login:
        print "if not social"    
        provider_name = ProviderName.query.filter_by(name=provider).one()
        user_profile = UsersProfile(screen_name=username,email=email)
        db.session.add(user_profile)
        db.session.commit()
        social = SocialLogin(social_login_id=social_id, name=username, email=email, provider_name_id=provider_name.id, users_id=user_profile.id)
        db.session.add(social)
        user_profile.current_login_at = user_profile.date_created
        user_profile.current_login_ip = "10.0.0.2"
        db.session.commit()
        login_user(user_profile, True)
    
    return redirect(url_for('users.index'))
    