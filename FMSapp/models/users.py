from  .. import db,login_manager
from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash ,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import datetime

#TO RETURN ANY VARIABLE FROM THE CHILD OR PARENT TABLE USE THE BACKREF option


class Roles(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    role_name=db.Column(db.String(50),unique=True,index=True)

    users=db.relationship('User',backref='role',lazy='dynamic')

    def __str__(self):
        return self.role_name

    def __repr__(self):
        return "<Role %r>" %self.role_name

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(50),nullable=False,index=True)
    lname=db.Column(db.String(50),nullable=False,index=True)
    password_hash=db.Column(db.String(128),nullable=False)
    email=db.Column(db.String(30),unique=True,nullable=False,index=True)
    created_on=db.Column(db.DateTime,index=True,default=datetime.datetime.utcnow,nullable=False)
    confirmed=db.Column(db.Boolean,default=False)

        #organization_name=db.Column(db.String(50),nullable=False,unique=True,index=True)

    # Organization to User
    organization_id=db.Column(db.Integer,db.ForeignKey('organization.id'),nullable=False)
    #organization_rel=db.relationship('Organization',foreign_keys=[organization_id])

    #role to user connection
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'),nullable=False)
    #role_rel=db.relationship('Roles',foreign_keys=[role_id])


    user_sub=db.relationship('Submissions',backref='usersub',lazy='dynamic')



        #def __init__(self,fname,lname,password,email,organization_name):
    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email==current_app.config["ADMIN_EMAIL"]:
                self.role=Roles.query.filter_by(role_name='admin').first()
            if self.role is None:
                self.role=Roles.query.filter_by(role_name='teacher').first()

        #    vars(self).update(kwargs)

        #    self.fname=fname
        #    self.lname=lname

        #    self.password=password
        #    self.email=email
        #    self.organization_name=organization_name

    @property
    def password(self):
        raise AttributeError("password is readonly")

    @password.setter
    def password(self,password):
       self.password_hash = generate_password_hash(password,method='pbkdf2:sha512',salt_length=64)

        #def set_role(self):


    def verify_password(self,password):
       return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self,expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')

    def confirm(self,token):

        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False

        self.confirmed=True
        db.session.add(self)
        #db.session.commit()
        return True

    def get_id(self):
        return self.id

    def get_role(self):

        return self.role


    def __repr__(self):
        return "<Users %r >" % self.fname





class Questions(db.Model):
    __tablename__='questions'
    id=db.Column(db.Integer,primary_key=True)
    question=db.Column(db.String(500),index=True,nullable=False)
    #from Organization to Questions
    organization_id=db.Column(db.Integer,db.ForeignKey('organization.id'),nullable=False)

    #from Question to Submissions
    question_sub=db.relationship('Submissions',backref='question_sub',lazy='dynamic')

    def __repr__(self):
        return "<Questions %r>" %self.question


class Organization(db.Model):
    __tablename__='organization'
    id=db.Column(db.Integer,primary_key=True)
    #user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    organization_domain=db.Column(db.String(25),unique=True,nullable=False,index=True)
    date_created=db.Column(db.DateTime,index=True,default=datetime.datetime.utcnow,nullable=False)

    #organization to User
    organization_rel_users=db.relationship('User',foreign_keys=[User.organization_id],
    backref=db.backref('organizationid',
    lazy='joined'),
    lazy='dynamic')

    #organization to Question
    #organization_rel_questions=db.relationship('Questions',backref='organization_question_id',lazy='dynamic')
    organization_rel_questions=db.relationship('Questions',foreign_keys=[Questions.organization_id],
    backref=db.backref('org_ques_id',lazy='joined'),
    lazy='dynamic')

    def __repr__(self):
        return "<Organization %r >" % self.organization_domain



class Stream(db.Model):
    __tablename__='streams'
    id=db.Column(db.Integer,primary_key=True)
    stream=db.Column(db.String(50),index=True,nullable=False,unique=True)
    sub_id=db.relationship('Submissions',backref='streamid',lazy='dynamic')

    def __repr__(self):
        return "<Stream %r>" %self.stream

class Submissions(db.Model):
    __tablename__='submissions'
    id=db.Column(db.Integer,primary_key=True)
    submission=db.Column(db.Integer,nullable=False,index=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    stream_id=db.Column(db.Integer,db.ForeignKey('streams.id'))
    question_id=db.Column(db.Integer,db.ForeignKey('questions.id'))

    def __repr__(self):
        return "<Submissions %r>" %self.submissions





#class UserLogin(UserMixin):
#    def __init__(self,**kwargs):
#        super(UserLogin,self).__init__(**kwargs)
#        self.user_id=None
#    def get_id(self):
#        return self.user_id
#    def get_role(self):
#        return self.role_id
#    def is_teacher(self):
#        return True if self.role == 'teacher' else False
#    def set_role(self, role):
#        self.role = role


#@login_manager.user_loader
#def load_user(user_id):
#    print("FROM USERs :: "+user_id )
#    return User.query.get(int(user_id))
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):

    user=User.query.get(int(user_id))

    #user=User.query.filter_by(id=int(user_id)).first()
    if not user:
        return
    #current_u=User()
    #current_u.user_id=user.id
    #current_u.role=user.role
    #return current_u

    return user
