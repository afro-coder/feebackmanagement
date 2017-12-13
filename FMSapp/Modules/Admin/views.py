#from . import admin_interface
from flask import request,render_template,url_for,redirect,flash
from flask_login import login_required
from ..utils import requires_roles
from flask_admin.contrib.sqla import ModelView
from ... import admin,db
from ...models.users import User
#@admin.route('/',methods=['GET','POST'])
#@login_required
#@requires_roles('teacher')
#def admin_default():
#    return render_template("admin/base.html")
admin.template_mode='bootstrap3'
admin.add_view(ModelView(User,db.session,endpoint='admin_interface'))
