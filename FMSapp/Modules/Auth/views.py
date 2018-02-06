from . import auth
from .forms import RegForm,LoginForm
from flask import request,render_template,url_for,redirect,flash,session
from flask_login import current_user,logout_user,login_required,login_user
from ...models.users import User,Organization
from FMSapp import db

#from FMSapp import sess
from ..utils import send_email

import os

@auth.before_app_request
def before_request():
    # print("\tREQUEST ENDPOINT ::"+str(request.endpoint))
    # print("\tREQUEST ARGS ::"+str(request.args.get('next')))
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))



@auth.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('viewhome.home'))

    form=RegForm()

    if form.validate_on_submit():

        user=User(fname=form.fname.data,
        lname=form.lname.data,
        email=form.email.data,
        #organization_name=form.username.data,
        password=form.password.data)
        organization=Organization(organization_domain=form.username.data)
        organization.organization_rel_users.append(user)
        db.session.add(user)
        db.session.add(organization)
        #db.session.commit()

        db.session.flush()
        token=user.generate_confirmation_token()
        try:
            send_email(user.email,'Confirm your Account','email/auth/confirm',user=user,token=token)
            flash('A confirmation Email has been sent, Please check your inbox','success')
            db.session.commit()
            return redirect(url_for('auth.login'))
        except Exception as e:
            print("LINE 48 EMAIL: "+str(e))
            db.session.rollback()
    print(form.errors)
    return render_template('auth/register.html',form=form)



@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('viewhome.home'))
    if current_user.confirm(token):
        print('\tENTERED')
        flash('Account confirmed ','success')
    else:
        flash('Invalid Link or Link has expired','warning')
    return redirect(url_for('viewhome.home'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token=current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm your account','email/auth/confirm',user=current_user,token=token)
    flash("A new confirmation email has been sent","success")
    return redirect(url_for('viewhome.home'))



@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('viewhome.home'))
    return render_template('auth/unconfirmed.html')

@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('viewhome.home'))
    form=LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            print("REQUEST ARGS "+str(request.args.get('next')))


            return redirect(request.args.get('next') or url_for('viewhome.home'))
        flash('Invalid username or password','info')
    return render_template('auth/login.html',form=form)
    #if form.validate_on_submit():
        #user=User.query.filter_by(email=form.email.data).first()
        #if user is not None and User.verify_password(form.password.data)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out","success")
    return redirect(url_for("viewhome.home"))

@auth.teardown_app_request
def end(self):
    db.session.close()
