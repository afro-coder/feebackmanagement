from flask import Blueprint


admin_interface=Blueprint('user_blueprint',__name__,url_prefix='/admin')
from . import views
