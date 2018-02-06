from flask import current_app, render_template,flash
from hashids import Hashids
from flask_mail import Message
from threading import Thread
from  FMSapp import mail
from flask_login import current_user
from flask import url_for, redirect
from functools import wraps
from ..models.users import User
import random,string



#app.config['MAIL_SUBJECT_PREFIX'] = '[OSFapp]'
#app.config['MAIL_SENDER'] = 'Flasky Admin <lmnography@gmail.com>'


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to,subject,template,**kwargs):
    app = current_app._get_current_object()
    msg=Message(current_app.config['MAIL_SUBJECT_PREFIX'] + subject,
    sender=current_app.config['MAIL_SENDER'],recipients=[to])
    msg.body=render_template(template +'.txt',**kwargs)
    msg.html=render_template(template +'.html',**kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # print("\t\t\t DECORAT ",*roles)
            # print(type(*roles))
            # print(type(current_user.get_role()))
            if str(current_user.get_role()) not in roles:

                # print("USER role",current_user.get_role())
                flash("Unauthorized")
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def generate_form_token(N):
    form_token=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

    return form_token
