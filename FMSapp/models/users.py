from  .. import db

class User(db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True,nullable=False)
    username=db.Column(db.String(64),unique=True,nullable=False,index=True)
    password_hash=db.Column(db.String(128),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)


    def __repr__(self):
        return "<Users %r >" % self.username
