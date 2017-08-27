from  .. import db

class User(db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True,nullable=False)
    username=db.Column(db.String(64),unique=True,nullable=False,index=True)
    password_hash=db.Column(db.String(128),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)

    def __init__(self,name,username,password_hash,email):
        self.name=name
        self.username=username
        self.password_hash=password_hash
        self.email=email

    @property
    def password():
        raise "password is readonly"
    
    def __repr__(self):
        return "<Users %r >" % self.username
