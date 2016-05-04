from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email,Regexp,EqualTo,ValidationError
from ..models import User

class LoginForm(Form):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('Password',validators=[Required()])
    remember_me=BooleanField('Keep me logined In')
    submit=SubmitField('Login in')

class RegisterForm(Form):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    username=StringField('Username',validators=[Required(),Regexp('^[a-zA-Z][a-zA-Z0-9_]*$',0,'Usernames must have only letters,numbers, dots or underscores')])
    password=PasswordField('Password',validators=[Required(),EqualTo('password2',message='passwords must match.')])
    password2=PasswordField('Confirm password',validators=[Required()])
    submit=SubmitField('Register')

    def valid_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("email has been registered")

    def valid_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')



