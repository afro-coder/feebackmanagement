from . import admin
#from flask import request,render_template,url_for,redirect,flash
#from flask_login import login_required
#from ..utils import requires_roles
from wtforms import PasswordField,TextField,Form
from flask_admin.contrib.sqla.fields import QuerySelectField
from wtforms.validators import InputRequired,EqualTo
from flask_admin.form import SecureForm
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView,expose,AdminIndexView
from ... import db
from ...models.users import (User,Questions,Roles,
Stream,Organization,Subject)
from werkzeug.security import generate_password_hash

#BaseView is not for models it is for a standalone-view
# ModelView is for Models
#AdminIndexView is for Admin Home page
class MyPassField(PasswordField):
    def process_data(self, value):
        self.data = ''  # even if password is already set, don't show hash here
        # or else it will be double-hashed on save
        self.orig_hash = value

    def process_fromdata(self, valuelist):
        value = ''
        if valuelist:
            value = valuelist[0]
        if value:
            self.data = generate_password_hash(
            value,method='pbkdf2:sha512',salt_length=64)
        else:
            self.data = self.orig_hash
    def __init__(self,name, **kwargs):
       # You can pass name and other parameters if you want to
       super(MyPassField, self).__init__(name,**kwargs)


class CustomModelView(ModelView):
    # def is_accessible(self):
        # return current_user.is_authenticated() and
        # current_user.is_admin()
    form_base_class=SecureForm



class UserView(CustomModelView):
    column_exclude_list=['password_hash',]
    form_excluded_columns=('user_sub')
    form_columns=('fname','lname','password',
    'confirm_password','email','created_on',
    'confirmed','organizationid','role')

    column_labels=dict(fname='First Name',
    lname='Last Name',password_hash='Password',
    organizationid='Organization',
    )

    form_overrides=dict(password=MyPassField)



    form_extra_fields={
    'password':MyPassField('Password',validators=[InputRequired(),EqualTo('confirm_password',
    message='Passwords must match ')]),
    'confirm_password':PasswordField('Confirm password',validators=[InputRequired()])
    }

    form_args=dict(password=dict(
    validators=[InputRequired(),EqualTo('confirm_password',
    message='Passwords must match ')]),

    confirm_password=dict(validators=[InputRequired()]),

    )


admin.add_view(UserView(User,db.session))
# admin.add_view(UserView(name='hello'))

class QuestionView(CustomModelView):
    column_exclude_list=['question_sub',]
    #form_excluded_columns
    column_labels=dict(question='Question',
    org_ques_id='Organization ID')
    form_args = {
        'org_ques_id': {
            #add a current user proxy right here
            'query_factory': lambda: db.session.query(Organization).filter_by(id = '1')
        }
    }

admin.add_view(QuestionView(Questions,db.session))

class StreamView(CustomModelView):
    form_columns=['stream',]
    form_excluded_columns=['submissions_id']

admin.add_view(StreamView(Stream,db.session))
class SubjectView(CustomModelView):
    form_excluded_columns=['submission_rel']
    column_labels=dict(streamsub='Stream')
    #form_columns=['stream','subjects',]
    #form_excluded_columns=['sub_id']
admin.add_view(SubjectView(Subject,db.session))


@admin.teardown_app_request
def close(self):
    db.session.close()
