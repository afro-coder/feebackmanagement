from flask import current_app, render_template
from hashids import Hashids
from  .. import mail
from flask_mail import Message
from threading import Thread

def create_hashid(id):
    hashids = Hashids(min_length=5, salt=current_app.config['SECRET_KEY'])
    hashid = hashids.encode(id)
    return hashid

def decode_hashid(hashid):
    hashids = Hashids(min_length=5, salt=current_app.config['SECRET_KEY'])
    id = hashids.decode(hashid)
    return id



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
