from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Email,EqualTo
from ...models.users import 

class RegForm(FlaskForm):
    name = StringField('Name',validators=[InputRequired()])
    password = PasswordField('Password',validators=[
    InputRequired(),
    EqualTo('password_check',message="Passwords must match")])

    password_check = PasswordField('Repeat Password',validators=[InputRequired()])
    email=StringField('email',validators=[InputRequired(),Email(message="invalid email")])
    submit=SubmitField('submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class LoginForm(FlaskForm):
    email=StringField('email',validators=[InputRequired(),Email(message="invalid email")])
    password = PasswordField('Password',validators=[InputRequired()])
