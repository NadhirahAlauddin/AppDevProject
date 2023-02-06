from wtforms import Form, StringField, SelectField, TextAreaField, validators, PasswordField
from wtforms.fields import EmailField
from flask_wtf import FlaskForm
import shelve
import re



def validate_password(form, field):
    if not re.search('\d', field.data):
        raise validators.ValidationError('Password must contain at least one number.')
    if not re.search('[A-Z]', field.data):
        raise validators.ValidationError('Password must contain at least a capital letter.')


def validate_existing_email(form, field):
    db = shelve.open('users.db', 'r')
    users_dict = db['Users']
    email_list = [emails.get_email_address() for emails in users_dict.values()]
    if field.data in email_list:
        raise validators.ValidationError('This email address is already in use.')


def validate_existing_username(form, field):
    db = shelve.open('users.db', 'r')
    users_dict = db['Users']
    username_list = [usernames.get_username() for usernames in users_dict.values()]
    if field.data in username_list:
        raise validators.ValidationError('This username is already in use.')



class RegisterForm(Form):
     first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
     last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
     email_add = EmailField('Email Address:',[validators.Email(), validators.DataRequired(), validators.DataRequired()]) #validate_existing_email was replaced with validators.DataRequired
     username = StringField('Username:',[validators.Length(min=1, max=150), validators.DataRequired(), validators.DataRequired() ]) #validate_existing_username was replaced with validators.DataRequired
     gender = SelectField('Gender', [validators.DataRequired()],choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
     password = PasswordField('Password:',[validators.Length(min=8, max=150), validators.InputRequired(), validate_password])
     confirm_password = PasswordField('Confirm Password:',[validators.EqualTo('password', message='Passwords must match'),validators.InputRequired()])

class LoginForm(FlaskForm):
    login_username = StringField('Username:', [validators.DataRequired(), validate_existing_username])
    login_password = PasswordField('Password:', [validators.InputRequired()])
