import datetime
from app import app, db
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import logout_user, current_user, login_user, login_required
from oauth import OAuthSignIn
from models import *
from .forms import * 


users_blueprint = Blueprint("users", __name__, template_folder="templates") 


# @users_blueprint.route('/index')
# def index():
#     return render_template('index.html')

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
    session.pop("logged_in", None)
    session.pop("session", None)
    flash("You have logged out.", "danger")
    referer = request.headers["Referer"]
    print referer
    return redirect(referer)

@users_blueprint.route("/forgot-password")
def forgot_password():
    return "forgot password"

@users_blueprint.route('/profile')
@login_required
def user_profile():
    connected_providers = db.session.query(ProviderName.name).join(SocialLogin).join(UsersProfile).filter_by(id=current_user.id).all()
    subquery = db.session.query(ProviderName.name).join(SocialLogin).join(UsersProfile).filter_by(id=current_user.id).subquery()
    unconnected_providers = db.session.query(ProviderName.name).filter(~ProviderName.name.in_(subquery)).all()
    todos = TodoItem.query.filter_by(users_id=current_user.id).all()
    return render_template('profile.html', connected_providers=connected_providers,
                           unconnected_providers=unconnected_providers, todos=todos)

@users_blueprint.route("/settings")
def user_settings():
    return "user settings"

@users_blueprint.route("/delete-user/", methods=["POST"])
@login_required
def delete_user():
    if request.method == "POST":
        db.session.query(UsersProfile).filter_by(id=current_user.id).delete()
        db.session.query(SocialLogin).filter_by(users_id=current_user.id).delete()
        db.session.query(UsersRegister).filter_by(users_id=current_user.id).delete()
        db.session.query(TodoItem).filter_by(users_id=current_user.id).delete()
        db.session.commit()
        session.clear()
        flash("You just deleted your account.", "danger")
        return redirect(url_for('users.index'))

@users_blueprint.route('/new-todo', methods=['GET', 'POST'])
@login_required
def new_todo():
    if request.method == 'POST':
        todo = TodoItem(
            name=request.form['name'],
            deadline_date=datetime.datetime.strptime(request.form['deadline_date'],"%m/%d/%Y").date(),
            users_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('users.user_profile'))
    return render_template('new-todo.html', page='new-todo')

@users_blueprint.route('/mark-done/<int:todo_id>', methods=['POST'])
@login_required
def mark_done(todo_id):
    print todo_id
    if request.method == 'POST':
        todo = TodoItem.query.filter_by(id=todo_id).one()
        print "line 113", todo.id, todo.name, todo.is_done
        todo.is_done = True
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('users.user_profile'))


@users_blueprint.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('rest.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@users_blueprint.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('rest.index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email, avatar = oauth.callback()
    print social_id, username, email, avatar
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('rest.index'))
    social_login = SocialLogin.query.filter_by(social_login_id=social_id).first()
    if social_login:
        print "if social"
        if not current_user.is_active:
            print "not user active"
            # has account and users signs back in with social account
            users = UsersProfile.query.filter_by(id=social_login.users_id).one_or_none()
            users.login_count += 1
            users.last_login_ip = users.current_login_ip
            users.last_login_at = users.current_login_at
            users.current_login_ip = "10.0.0.1"
            users.current_login_at = datetime.datetime.now()
            db.session.add(users)
            db.session.commit()
            login_user(users, True)
        elif current_user.is_active:
            if social_login.social_login_id == social_id:
                print "if social_login.social_login_id == social_id"
                td = TodoItem.query.filter_by(users_id=social_login.users_id).all()
                if td:
                    for t in td:
                        t.users_id = current_user.id 
                        db.session.add(t)
                        db.session.commit()
                social_login.users_id = current_user.id
                db.session.add(social_login)
                db.session.commit()
            else:
                print "current user active"
                # has at least one account and is active and wants to connect more
                user_profile = UsersProfile.query.filter_by(id=current_user.id).first()
                provider_name = ProviderName.query.filter_by(name=provider).first()
                print "else make new SocialLogin"
                s_l = SocialLogin(social_login_id=social_id, name=username, email=email, avatar=avatar, users_id=user_profile.id, provider_name_id=provider_name.id)
                db.session.add(s_l)
                db.session.commit()
            return redirect(url_for("rest.index"))
    if not social_login:
        print "if not social"    
        if not current_user.is_active:
            print "not user active"
            # user logins in with social for first time and is not currently loggged in under any other account
            provider_name = ProviderName.query.filter_by(name=provider).one()
            user_profile = UsersProfile(screen_name=username,email=email, avatar=avatar)
            db.session.add(user_profile)
            db.session.commit()
            check_exist_social_login_id = SocialLogin.query.filter_by(social_login_id=social_id).one_or_none()
            if not check_exist_social_login_id: 
                social = SocialLogin(social_login_id=social_id, name=username, email=email, avatar=avatar, provider_name_id=provider_name.id, users_id=user_profile.id)
                db.session.add(social)
                user_profile.current_login_at = user_profile.date_created
                user_profile.current_login_ip = "10.0.0.2"
                db.session.commit()
                login_user(user_profile, True)
        elif current_user.is_active:
            print "current user active"
            #has a basic account and is logged in and wants to connect social accounts.
            user_profile = UsersProfile.query.filter_by(id=current_user.id).first()
            provider_name = ProviderName.query.filter_by(name=provider).first()
            social_login = SocialLogin(social_login_id=social_id, name=username, email=email, avatar=avatar, users_id=user_profile.id, provider_name_id=provider_name.id)
            db.session.add(social_login)
            db.session.commit()
            return redirect(url_for("users.user_profile"))
    return redirect(url_for('rest.index'))
    