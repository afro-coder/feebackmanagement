from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField,RadioField,FieldList,FormField,TextField
from wtforms.validators import InputRequired,DataRequired,ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ...models.users import Stream,User,Subject,Questions
from FMSapp import db

def get_subject():
    return Subject.query
class QuestionSelect(FlaskForm):

    subject_data=QuerySelectField('Stream',
    allow_blank=True,blank_text="Enter ",validators=[DataRequired('Required Field')])
    teacher_select=SelectField('Teacher',validators=[DataRequired('Required Field')],render_kw={'disabled':'disabled'})





    submit=SubmitField('submit')


class QuestionRadio(FlaskForm):
    rad=RadioField("rad",choices=[(1,'Yes'),(2,'No')],id="opt")
class QuestionForm(FlaskForm):
    options=FieldList(FormField(QuestionRadio),min_entries=0)

    # @classmethod
    # def append_field(cls, name, field):
    #     setattr(cls, name, field)
    #     return cls
