from . import admin
#from flask import request,render_template,url_for,redirect,flash
#from flask_login import login_required
#from ..utils import requires_roles
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView,expose
from ... import db
from ...models.users import User



class UserView(ModelView):
    can_delete=False
    can_view_details = False
    create_modal = True
    edit_modal = True
    #column_exclude_list=['password_hash']
    #@expose('/')
    #def index(self):
    #    return self.render('admin/index.html')
    # pass
    #def is_accessible(self):
    #    return current_user.is_authenticated

admin.add_view(UserView(User,db.session))
# admin.add_view(UserView(name='hello'))
