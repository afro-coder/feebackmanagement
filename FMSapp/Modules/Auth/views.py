from . import auth
from .forms import RegForm,LoginForm
from flask import request,render_template,url_for,redirect,flash,session
from flask_login import current_user,logout_user,login_required,login_user
from ...models.users import User,Domains
from FMSapp import db

#from FMSapp import sess
from ..utils import send_email

import os

#Change the flow to registration then sending  a link to activate the user, then creating a
# Domain name for them using their username
#Then loading their admin page
#
@auth.before_app_request
def before_request():
    print("\tREQUEST ENDPOINT ::"+str(request.endpoint))
    print("\tREQUEST ARGS ::"+str(request.args.get('next')))
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

        user=User(
        email=form.email.data,
        organization_name=form.username.data,
        password=form.password.data)
        db.session.add(user)
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
        flash('Invalid Link or Link has expired','Warning')
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
        flash('Invalid username or password')
    return render_template('auth/login.html',form=form)
    #if form.validate_on_submit():
        #user=User.query.filter_by(email=form.email.data).first()
        #if user is not None and User.verify_password(form.password.data)

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.','success')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.','success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)

@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out","success")
    return redirect(url_for("viewhome.home"))
