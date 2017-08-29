from . import auth
from .forms import RegForm,LoginForm
from flask import request,render_template,url_for,redirect,flash
from ...models.users import User
from FMSapp import db
@auth.route('/register', methods=['GET','POST'])
def register():
    form=RegForm()
    if form.validate_on_submit():
        enter=User(username=form.username.data,
        fname=form.fname.data,
        lname=form.lname.data,
        email=form.email.data,
        password_hash=form.password.data)
        db.session.add(enter)
        return redirect(url_for('viewhome.home'))

    return render_template('Landing/Regform.html',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()

    if form.validate_on_submit():
        pass
