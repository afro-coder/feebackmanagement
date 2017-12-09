from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import InputRequired,Email,EqualTo,ValidationError,Regexp,Length,DataRequired
from ...models.users import User

class LoginForm(FlaskForm):
    email=StringField('email',validators=[InputRequired(),Length(1,64),Email(message="invalid email")])

    password = PasswordField('Password',validators=[InputRequired()])

    remember_me=BooleanField('Keep me logged in')

    submit_log=SubmitField('Log in')

class RegForm(FlaskForm):
    #username = StringField('Username',validators=[InputRequired(),
    #Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, '
    #                                        'numbers, dots or underscores')])
    fname=StringField('First Name',validators=[InputRequired()])
    lname=StringField('Last Name',validators=[InputRequired()])
    username=StringField('Username',validators=[InputRequired(),Regexp('(([a-zA-Z0-9])(-[a-zA-Z0-9])*)')])

    password = PasswordField('Password',validators=[InputRequired(),
    EqualTo('password_check',message="Passwords must match")])

    password_check = PasswordField('Repeat Password',validators=[InputRequired()])

    email=StringField('email',validators=[InputRequired(),Length(1,64),Email(message="invalid email")])

    submit_reg=SubmitField('submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    #def validate_username(self, field):
    #    if User.query.filter_by(organization_name=field.data).first():
    #        raise ValidationError('Username already in use.')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])

    password = PasswordField('New password', validators=[
    DataRequired(), EqualTo('password2', message='Passwords must match.')])

    password2 = PasswordField('Confirm new password',validators=[DataRequired()])
    submit = SubmitField('Update Password')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    submit = SubmitField('Reset Password')

class PasswordResetForm(FlaskForm):
    password=PasswordField('New Password', validators=[
       DataRequired(), EqualTo('password2', message='Passwords must match')])

    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit_dom=SubmitField('Reset Password')

class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
