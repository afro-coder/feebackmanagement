from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Email


class RegForm(FlaskForm):
    name = StringField('Name',validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()])
    email=StringField('email',validators=[InputRequired(),Email(message="invalid email")])
    submit=SubmitField('submit')

class LoginForm(FlaskForm):
    email=StringField('email',validators=[InputRequired(),Email(message="invalid email")])
    password = PasswordField('Password',validators=[InputRequired()])
