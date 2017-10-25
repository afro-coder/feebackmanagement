from  .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash ,check_password_hash
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(50),nullable=False,unique=True)
    lname=db.Column(db.String(50),nullable=False,unique=True)

    password_hash=db.Column(db.String(128),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)


    def __init__(self,fname,lname,password,email):
        self.fname=fname
        self.lname=lname
        #self.username=username
        self.password=password
        self.email=email

    @property
    def password(self):
        raise AttributeError("password is readonly")

    @password.setter
    def password(self,password):
       self.password_hash = generate_password_hash(password,method='pbkdf2:sha512',salt_length=64)


    def verify_password(self, password):
       return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return "<Users %r >" % self.fname
