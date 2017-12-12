from flask import Blueprint


admin_interface=Blueprint('admin',__name__,url_prefix='/admin')
from . import views
