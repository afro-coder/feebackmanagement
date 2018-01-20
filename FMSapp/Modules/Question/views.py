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

@question.route("/stream/<hashid>/<semester>", methods=['GET', 'POST'])
def display_question(hashid,semester):

    dec=decode_hashid(hashid=hashid)
    (dec,)=dec
    stream_id=dec
    print(stream_id)

    dec1=decode_hashid(hashid=semester)
    (dec1,)=dec1
    semester_id=dec1
    print(semester_id)

    subjects= Subject.query.filter_by(stream=dec,semester=dec1)


    question=[(ques.id,ques.question) for ques in Questions.query.all()]
    form=QuestionSelect()
    form.subject_data.query=subjects
    form.teacher_select.choices=[]

    # if form.validate_on_submit():
    #     print("\t\t\t\t TRUE")
    #     return "Success"

    form_id=generate_form_token(12)
    session["form_id"]=form_id

    return render_template('question/question_display.html',form=form,question=question,hashid=hashid,form_id=form_id)


@question.route('/_gen_teachers',methods=['GET','POST'])
def gen_teacher():
    if request.method == "GET":
        subject_id=request.args.get('b',0,type=int)
        print(subject_id)

        t=[(row.id,row.fname)  for row in  User.query.filter(User.sub_id.any(id=subject_id)).all()]


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
        # for key,value in d.items():
        #     print(key+":::"+value)


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
    return render_template("question/success.html")
@question.route('/test_question',methods=["GET","POST"])
def testques():

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
    # print(d)
    # # for key in dict:
    #     # print(key.startswith('options'))
    #     # print("\n")
    #     # print('form key '+dict[key])

    return "Sucess"
