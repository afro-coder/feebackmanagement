from . import admin
from flask import request,url_for,redirect,jsonify,make_response
from  ...mod_util import create_hashid

#from flask_login import login_required
#from ..utils import requires_roles

from wtforms import PasswordField,TextField,Form
from flask_admin.contrib.sqla.fields import QuerySelectField
from wtforms.validators import InputRequired,EqualTo
from flask_admin.form import SecureForm
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView,expose,AdminIndexView
from ... import db,charts
from ...models.users import (User,Questions,Roles,
Stream,Organization,Subject,Submissions)
from werkzeug.security import generate_password_hash

from .forms import SubmissionForm
from flask_googlecharts import PieChart

#BaseView is not for models it is for a standalone-view
# ModelView is for Models
#AdminIndexView is for Admin Home page

#try using ajax for loading fields
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
    # IF you enable CsrfProtect switch to wtforms Form class instead of secure form
    # form_base_class=SecureForm
    form_base_class=Form



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
    created_on=dict(render_kw={'disabled':'disabled'})

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
    #RECHECK HERE
    form_excluded_columns=['submission_rel']
    column_labels=dict(streamsub='Stream',teachersubj='Teacher')
    #form_columns=['stream','subjects',]
    #form_excluded_columns=['sub_id']
admin.add_view(SubjectView(Subject,db.session))

class LinkView(BaseView):
    @expose('/',methods=['GET','POST'])
    def index(self):
        #formdata=[(stream.id,stream.stream) for stream in Stream.query.all()]
        form=StreamForm()

        #form=StreamForm(stream=formdata)
        return self.render('admin/link.html',form=form)

    @expose('/_generatelink',methods=['GET'])
    def genlink(self):
        if request.method == "GET":

            stream_name=request.args.get('b',0,type=int)
            print(stream_name)


            print(request.script_root)
            url=url_for('question.display_question',hashid=create_hashid(stream_name))
            print(url)


        return jsonify(d=url)




admin.add_view(LinkView(name='Generate Link',endpoint='linkgen'))

class  SubmissionView(CustomModelView):
    pass
admin.add_view(SubmissionView(Submissions,db.session))

class ResultsView(BaseView):
    @expose('/')
    def index(self):

        # my_chart=PieChart("new_chart",options={'title': 'My Chart', "width": 500,"height": 300,"is3D":True})
        # ans_yes=Submissions.query.filter_by(submission=1,question_id=1,user_id=2).count()
        # ans_no=Submissions.query.filter_by(submission=2,question_id=1,user_id=2).count()
        # print("\t\t\tANS_YES",ans_yes)
        # print("\t\t\tANS_No",ans_no)
        # my_chart.add_column("string", "Answer")
        # my_chart.add_column("number", "percent")
        # my_chart.add_rows([["Yes", ans_yes],
        #                 ["NO", ans_no],
        #                 ])
        # charts.register(my_chart)
        form=SubmissionForm()

        form.subject_select.choices=[(0,"Select a Subject")]
        form.teacher_select.choices=[(0,"Select a Teacher")]
        question=[(ques.id,ques.question) for ques in Questions.query.all()]

        return self.render('admin/results.html',form=form,question=question)
    @expose('/_submissions',methods=["GET"])
    def submissions(self):
        if request.method=="GET":
            try:
                stream_id=request.args.get('b',0,type=int)



                data=[(dat.id,dat.subject_name) for dat in Subject.query.filter_by(stream=stream_id)]
                print(data)
                return jsonify(data)
                # if len(subject_id) > 0:
                #     # data=[(dat.id,dat.subject_name) for dat in Subject.query.filter_by(stream=stream_id)]
                #     data=[(row.id,row.fname)  for row in  User.query.filter(User.subject_det.any(id=subject_id)).all()]
                #     print(data)
                #     return jsonify(data)

            except Exception as e:
                return jsonify(success=0, error_msg=str(e))


    @expose('/_charts',methods=["GET","POST"])
    def load_chart(self):
        stream_id=request.args.get('stream',0,type=int)
        subject_id=request.args.get('subject',0,type=int)
        teacher_id=request.args.get('teacher',0,type=int)
        question=[(ques.id,ques.question) for ques in Questions.query.all()]
        chart_data=[]
        dictv =request.form.to_dict()
        dictv.pop('csrf_token')

        print(dictv)
        print(request.json)
        for key,value in question:
            ans_yes=Submissions.query.filter_by(submission=1,question_id=key,subject_id=dictv['subject_select'],user_id=dictv['teacher_select']).count()
            ans_no=Submissions.query.filter_by(submission=2,question_id=key,subject_id=dictv['subject_select'],user_id=dictv['teacher_select']).count()
            # ans_no=Submissions.query.filter_by(submission=2,question_id=key,subject_id=subject_id,user_id=teacher_id).count()
            my_chart=PieChart("teacher_chart"+str(key),options={'title': 'Submission', "width": 500,"height": 300,"is3D":True})
            my_chart.add_column("string", "Answer")
            my_chart.add_column("number", "percent")
            print("\t\t\t",ans_no)
            print("\t\t\t",ans_yes)
            my_chart.add_rows([["Yes", ans_yes],["NO", ans_no]])
            chart_data.append((my_chart.name,key,value))

            charts.register(my_chart)

        print(chart_data )
        return self.render('admin/result_chart.html',stream_id=stream_id,question=question,chart_data=chart_data),"success"
    #pass a list of variables and the then convert them to jinja

admin.add_view(ResultsView(name='Results',endpoint='results'))

@admin.teardown_app_request
def close(self):
    db.session.close()
