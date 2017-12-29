from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from ...models.users import Stream




class StreamForm(FlaskForm):
    #stream=QuerySelectField('Stream',allow_blank=True,query_factory=lambda:Stream.query.all())
    stream=QuerySelectField('Stream',allow_blank=True,blank_text=u'Select a Stream',
    query_factory=lambda: Stream.query.all(),validators=[DataRequired()])

    submit=SubmitField('Submit')
