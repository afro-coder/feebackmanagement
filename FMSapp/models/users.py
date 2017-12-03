from  .. import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash ,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(50),nullable=False,unique=False)
    lname=db.Column(db.String(50),nullable=False,unique=False)
    organization_name=db.Column(db.String(50),nullable=False,unique=True,index=True)
    password_hash=db.Column(db.String(128),nullable=False)
    email=db.Column(db.String(30),unique=True,nullable=False,index=True)
    confirmed=db.Column(db.Boolean,default=False)
    rel=db.relationship('Domains',backref='users',lazy=True)


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
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        print("\tCONFIRM TOKEN FUNCTION")
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            print("\tERROR HERE IN LINE 48")
            return False
        if data.get('confirm') != self.id:
            print("DEBUG:: " + int( self.id))
            return False
        print('\t\tLINE 54 REACHED')
        self.confirmed=True
        db.session.add(self)
        db.session.commit()
        return True



    def __repr__(self):
        return "<Users %r >" % self.organization_name

class Domains(db.Model):
    __tablename__='domains'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    domains=db.Column(db.String(25),unique=True,nullable=False)

    def __init__(self,user_id,domain):
        self.user_id=user_id
        self.domains=domain

    def __repr__(self):
        return "<Domains %r >" % self.domains


@login_manager.user_loader
def load_user(user_id):
    print("FROM USERs :: "+user_id )
    return User.query.get(int(user_id))
