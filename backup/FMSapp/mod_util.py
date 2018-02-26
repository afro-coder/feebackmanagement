from flask import current_app
from hashids import Hashids
import os
# common=os.urandom(16).hex()
def create_hashid(id):
    hashids = Hashids(min_length=6, salt=str(current_app.config['SECRET_KEY']))
    # hashids = Hashids(min_length=6, salt=common)
    hashid = hashids.encode(id)
    return hashid

def decode_hashid(hashid):
    hashids = Hashids(min_length=6, salt=str(current_app.config['SECRET_KEY']))
    # hashids = Hashids(min_length=6, salt=common)
    id = hashids.decode(hashid)
    return id
