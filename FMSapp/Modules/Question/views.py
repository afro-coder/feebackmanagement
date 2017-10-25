from . import question
from flask import request,render_template,url_for,redirect,flash

#add a url converter here
@question.route("/")
def display_question():
    teacher_names=['Prof A','Prof B','Prof C','Prof D','Prof E']
    semesters=['Sem 1','Sem 2','Sem 3','Sem 4','Sem 5','Sem 6']
    questions=['Does the lecturer communicate clearly? .','Is the lecturer confident in dealing with the subject matter?.',
    'Is the lecturer able to maintain order and discipline? .','Does the lecturer come on time for a lecture? .']
    quest_dict=dict(enumerate((question for question in questions),start=1))
    return render_template('question/question.html',quest_dict=quest_dict,teacher_names=teacher_names,semesters=semesters)
