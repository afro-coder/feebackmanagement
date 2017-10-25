from . import auth
from .forms import RegForm,LoginForm
from flask import request,render_template,url_for,redirect,flash
from ...models.users import User
from FMSapp import db

@auth.route('/entry',methods=['GET','POST'])
def entry():
    form=RegForm()
    form1=LoginForm()
    return render_template('Landing/entry.html',form=form,form1=form1)
@auth.route('/register', methods=['GET','POST'])
def register():
    form=RegForm()
    form1=LoginForm()

    if form.validate_on_submit():
        enter=User(
        fname=form.fname.data,
        lname=form.lname.data,
        email=form.email.data,
        password=form.password.data)
        db.session.add(enter)
        db.session.commit()

        flash('Sucess','success')
        return redirect(url_for('viewhome.home'))
    else:
        flash('Error','info')
        error1=True
        return render_template('Landing/entry.html',form=form,form1=form1,error1=error1)



    return render_template('Landing/entry.html',form=form,form1=form1)

@auth.route('/login',methods=['GET','POST'])
def login():
    form1=LoginForm()
    #if form1.validate_on_submit():
    #    user=User.query.filter_by(email=form1.email.data)
    #    if user  is not None and User.verify_password(form1.data.password):
    #        flash("Success")
    if form1.validate_on_submit():
        user=User.query.filter_by(email=request.form.get['email'])
        if user  is not None and User.verify_password(request.form.get['password']):
            flash('Success')


    return render_template('Landing/index.html',form1=form1)
    #if form.validate_on_submit():
        #user=User.query.filter_by(email=form.email.data).first()
        #if user is not None and User.verify_password(form.password.data)
