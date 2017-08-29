from  .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(50),nullable=False,unique=True)
    lname=db.Column(db.String(50),nullable=False,unique=True)
    username=db.Column(db.String(64),unique=True,nullable=False,index=True)
    password_hash=db.Column(db.String(128),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)

    def __init__(self,fname,lname,username,password_hash,email):
        self.fname=fname
        self.lname=lname
        self.username=username
        self.password_hash=password_hash
        self.email=email

    @property
    def password():
        raise "password is readonly"

    @password.setter
    def password(self, password):
       self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
       return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return "<Users %r >" % self.username
