from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField, SubmitField
from wtforms.fields import EmailField, DateField
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



class RegisterForm(FlaskForm):
     email_address = EmailField('Email Address:',
                                [validators.Email(), validators.DataRequired(), validate_existing_email])
     username = StringField('Username:',
                            [validators.Length(min=1, max=150), validators.DataRequired(), validate_existing_username])
     password = PasswordField('Password:',
                              [validators.Length(min=8, max=150), validators.InputRequired(), validate_password])
     confirm_password = PasswordField('Confirm Password:',
                                      [validators.EqualTo('password', message='Passwords must match'),
                                       validators.InputRequired()])

class LoginForm(FlaskForm):
    login_username = StringField('Username:', [validators.DataRequired(), validate_existing_username])
    login_password = PasswordField('Password:', [validators.InputRequired()])
