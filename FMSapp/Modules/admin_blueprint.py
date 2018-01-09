from flask import Blueprint,url_for,redirect,request
# from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin,AdminIndexView,expose
from flask_admin.base import MenuLink
from flask_login import current_user
from .utils import requires_roles
# class LoginMenuLink(MenuLink):
#
#     def is_accessible(self):
#         return not current_user.is_authenticated


class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

class MyHomeView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login',next=request.url))

    @expose('/')

    def index(self):
        return self.render('admin/index.html')

class AdminBlueprint(Blueprint):
    views=None


    def __init__(self,*args, **kargs):
        self.views = []
        #return super(AdminBlueprint, self).__init__('admin1', __name__,url_prefix='/admin1',static_folder='static', static_url_path='/static/admin')
        return super().__init__('admin_user', __name__,
        #url_prefix='/admin1',
        static_folder='static',
        static_url_path='/static/',
        template_folder='templates'

        )


    def add_view(self, view):
        self.views.append(view)

    def register(self,app, options, first_registration=False):
        print(app)
        #admin = Admin(app, name='FMSAdmin', template_mode='bootstrap3',url='/admin',static_url_path='/static/admin')
        admin = Admin(app,url='/admin',name='FeedBack App',index_view=MyHomeView(name='Home',template='admin/index.html',endpoint='admin'), template_mode='bootstrap3')
        admin.add_link(LogoutMenuLink(name='Logout', category='', url="/auth/logout"))
        # admin.add_link(LoginMenuLink(name='Login', category='', url="/login"))
        # admin = Admin(app,url='/admin',template_mode='bootstrap3')

        for v in self.views:
            admin.add_view(v)
        #return super(AdminBlueprint, self).register(app, options, first_registration)
        return super().register(app, options, first_registration)
