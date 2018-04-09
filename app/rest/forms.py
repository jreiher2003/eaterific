from flask_wtf import FlaskForm 
from wtforms.validators import Email, Length, EqualTo, DataRequired 
from wtforms import PasswordField, BooleanField, SubmitField, TextField 
# from wtforms.fields.html5 import EmailField 
# from app.users.models import UsersRegister, SocialLogin, UsersProfile

# def validate_username(form, field): 
#     user = UsersRegister.query.filter_by(username=field.data).first()
#     if user:
#         field.errors.append("Username already registered!")
#         return False
#     return True

# def validate_email(form, field):
#     user = UsersRegister.query.filter_by(email=field.data).first()
#     user_profile = UsersProfile.query.filter_by(email=field.data).first()
#     if user:
#         field.errors.append("Email already registered!")
#         return False
#     if user_profile:
#         social = SocialLogin.query.filter_by(users_id=user_profile.id).all()
#         for s in social:
#             if s.email == field.data:
#                 field.errors.append("That email is already associated with your %s login." % s.provider_name.name)
#                 return False
#     return True

class SearchForm(FlaskForm):
    search = TextField("Search")
    submit = SubmitField("Search")

# class RegisterForm(FlaskForm):
#     username = TextField("Username",  [DataRequired(), validate_username])
#     email = EmailField("Email", [DataRequired(), Email(), validate_email])
#     password = PasswordField("Password", [DataRequired(), Length(min=6, message="The min password length is 6 chars long.")])
#     password_confirm = PasswordField("Confirm", [DataRequired(), EqualTo("password", message="Your passwords don't match.")])
#     submit = SubmitField("Register")