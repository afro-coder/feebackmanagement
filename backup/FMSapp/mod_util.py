from flask import current_app
from hashids import Hashids

def create_hashid(id):
    hashids = Hashids(min_length=6, salt=str(current_app.config['SECRET_KEY']))
    hashid = hashids.encode(id)
    return hashid

def decode_hashid(hashid):
    hashids = Hashids(min_length=6, salt=str(current_app.config['SECRET_KEY']))
    id = hashids.decode(hashid)
    return id
