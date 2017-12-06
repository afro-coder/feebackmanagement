from  .. import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash ,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import datetime

class Roles(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),unique=True)
class Organization(db.Model):
    __tablename__='organization'
    id=db.Column(db.Integer,primary_key=True)
    #user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    domain=db.Column(db.String(25),unique=True,nullable=False)
    organization_rel=db.relationship('Users',backref='organization_id',lazy='dynamic')

    def __init__(self,user_id,domain):
        self.user_id=user_id
        self.domains=domain



    def __repr__(self):
        return "<Domains %r >" % self.domains

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(50),nullable=False,index=True)
    lname=db.Column(db.String(50),nullable=False,index=True)
    #organization_name=db.Column(db.String(50),nullable=False,unique=True,index=True)
    organization_id=db.Column(db.Integer,db.ForeignKey('organization.id'),nullable=False)
    password_hash=db.Column(db.String(128),nullable=False)
    email=db.Column(db.String(30),unique=True,nullable=False,index=True)
    created_on=db.Column(db.DateTime,index=True,server_default=datetime.utcnow)
    confirmed=db.Column(db.Boolean,default=False)



    #def __init__(self,fname,lname,password,email,organization_name):
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

    def generate_reset_token(self, expiration=3600):
       s = Serializer(current_app.config['SECRET_KEY'], expiration)
       return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True



    def __repr__(self):
        return "<Users %r >" % self.organization_name




@login_manager.user_loader
def load_user(user_id):
    print("FROM USERs :: "+user_id )
    return User.query.get(int(user_id))
