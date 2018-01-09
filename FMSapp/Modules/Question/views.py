from . import question
from flask import request,render_template,url_for,redirect,flash,jsonify,abort
from ...models.users import User,Stream,Subject,Questions,Submissions
from .forms import QuestionSelect,QuestionForm,QuestionRadio
from ...mod_util import decode_hashid
from wtforms.validators import ValidationError
from flask import session
from FMSapp import db
from FMSapp.Modules.utils import generate_form_token

#add a url converter here
@question.before_request
def before_req():
    pass

@question.route("/stream/<hashid>", methods=['GET', 'POST'])
def display_question(hashid):
    # teacher_names=['Prof A','Prof B','Prof C','Prof D','Prof E']
    # semesters=['Sem 1','Sem 2','Sem 3','Sem 4','Sem 5','Sem 6']
    # questions=['Does the lecturer communicate clearly? .','Is the lecturer confident in dealing with the subject matter?.',
    # 'Is the lecturer able to maintain order and discipline? .','Does the lecturer come on time for a lecture? .']
    # quest_dict=dict(enumerate((question for question in questions),start=1))
    # return render_template('question/question.html',quest_dict=quest_dict,teacher_names=teacher_names,semesters=semesters)
    dec=decode_hashid(hashid=hashid)
    (dec,)=dec
    print("CHECK THIS")
    print(str(dec))
    stream_id=dec
    subjects= Subject.query.filter_by(stream=dec)

    question=[(ques.id,ques.question) for ques in Questions.query.all()]
    form=QuestionSelect()
    form.subject_data.query=subjects
    form.teacher_select.choices=[]
    # streamdata=dict(enumerate((stream for stream  in Stream.query.all()),start=1))
    #form.subject_select.choices=[('Hekk','Waa'),('Taa','gg')]

    if form.validate_on_submit():
        print("\t\t\t\t TRUE")
        return "Success"

    form_id=generate_form_token(12)
    session["form_id"]=form_id
    print("When Page is loaded",session["form_id"])

    # print("Session value")
    # print(session["form_id"])
    # print(form.errors)
    print(form.subject_data.data)

    return render_template('question/question_display.html',form=form,question=question,hashid=hashid,form_id=form_id)


@question.route('/_gen_teachers',methods=['GET','POST'])
def gen_teacher():
    if request.method == "GET":
        subject_id=request.args.get('b',0,type=int)
        print(subject_id)
        #teacher = Subject.query.filter(Subject.teacher.any(fname='phil'))
        #teacher = Subject.query.filter(Subject.teacher.any(fname='phil'))
        # t=[(row.) ]
        # t=[(row.id,row.fname) for row in  User.query.filter(User.subject_det.any(id=subject_id)).all()]
        # t=[(row.id,row.fname)  for row in  User.query.filter(User.subject_det.any(id=subject_id)).all()]
        t=[(row.id,row.fname)  for row in  User.query.filter(User.sub_id.any(id=subject_id)).all()]
        #a=[b[0] for b in t ]
        print(t)
        return jsonify(t)

    if request.method == "POST":
        #datasub=Submissions()
        dictv =request.form.to_dict()
        print(dictv)
        dictv.pop('csrf_token')
        print("debug")
        print(dictv)
        d={key[-1:]:dictv[key] for key in dictv if key.startswith('options')}
        if d is None:
            abort(405)
        for key,value in d.items():
            print(key+":::"+value)

        # try:
        #     for key,value in d.items():
        #         print("in the func")
        #         datasub.form_id=session["form_id"]
        #         datasub.user_id=int(dictv["teacher_select"])
        #         datasub.subject_id=int(dictv["subject_select"])
        #         datasub.stream_id=int(decode_hashid(dictv["stream_id"]))
        #         datasub.question_id=int(key)
        #         datasub.submission=int(value)
        #         db.session.add(datasub)
        #         db.session.commit()
        # except Exception as e:
        #     print("Success")
        #     if session["form_id"] != dictv["form_id"]:
        #         print(e)
                    # db.session.rollback()
        stream=decode_hashid(dictv["stream_id"])
        print(dictv["stream_id"])
        (stream,)=stream

        # if session["form_id"] != dictv["form_id"]:
        #     return False
        # session["dict_form_id"]=dictv["form_id"]
        # print("\t\t\After Posting",session["dict_form_id"])
        #
        for key,value in d.items():
            datasub=Submissions()

            datasub.form_id=dictv["form_id"]
            datasub.user_id=int(dictv["teacher_select"])
            datasub.subject_id=int(dictv["subject_data"])
            datasub.stream_id=int(stream)
            datasub.question_id=int(key)
            datasub.submission=int(value)
            if key == "1":
                datasub.suggestions=dictv["suggestions"]
            db.session.add(datasub)
        db.session.commit()


        # for key,value in dictv.items():
        #     print(key[-1:]+"::"+value)

        # print(dictv)
        print("success")
        jsondata=[{'type':'success','message':'success'}]
        return jsonify(jsondata)

    abort(405)




        # t={(row.fname,row.teacherid.__dict__) for row in User.query.join(User.subjectid).filter(User.id==Subject.id)}
        # print(p)
        # print(t)
@question.route('/success')
def suc():
    return "Thank you"
@question.route('/test_question',methods=["GET","POST"])
def testques():
    # questions=dict(enumerate((ques.question for ques in Questions.query.all()),start=1))
    # question=[{str(ques.id):ques.question} for ques in Questions.query.all()]
    # question=[{'id':'f'+str(ques.id),'question':ques.question} for ques in Questions.query.all()]
    question=[(ques.id,ques.question) for ques in Questions.query.all()]
    #form=QuestionForm()

    # print(question)

    form=QuestionForm()
    form.options.append_entry(RadioField("ra"))
    #test=[a for a in dir(form.options) if not a.startswith('__')]
    #print(test)

    return render_template('question/questiondisp.html',form=form,question=question)
@question.route('/_subform',methods=["GET","POST"])
def subform():
    print("Hello")
    dictv = request.form.to_dict()
    print(dictv)
    dictv.pop('csrf_token')
    print(dictv)
    d={key[-1:]:dictv[key] for key in dictv if key.startswith('options')}
    print(d)
    # for key in dict:
        # print(key.startswith('options'))
        # print("\n")
        # print('form key '+dict[key])

    return "Sucess"
