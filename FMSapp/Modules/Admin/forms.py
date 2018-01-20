from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import SubmitField,SelectField
from wtforms.validators import DataRequired
from ...models.users import Stream,Semester




class StreamForm(FlaskForm):
    #stream=QuerySelectField('Stream',allow_blank=True,query_factory=lambda:Stream.query.all())
    stream=QuerySelectField('Stream',allow_blank=True,blank_text=u'Select a Stream',
    query_factory=lambda: Stream.query.all(),validators=[DataRequired()])

    semester=QuerySelectField('Semester',allow_blank=True,blank_text=u'Select a Semester',
    query_factory=lambda: Semester.query.all(),validators=[DataRequired()])


    # submit=SubmitField('Submit')

class SubmissionForm(StreamForm):
    subject_select=SelectField('Subject',validators=[DataRequired('Required Field')],
    render_kw={'disabled':'disabled'})

    teacher_select=SelectField('Teacher',validators=[DataRequired('Required Field')],
    render_kw={'disabled':'disabled'})
