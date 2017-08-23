from  FMSapp import db

class User(db.Model):
    name=db.Column(db.string())
