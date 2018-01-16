from flask import Flask
from .mod_util import create_hashid
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,url_for,session
import os
from flask_login import LoginManager
from flask_sessionstore import Session
from flask_mail import Mail
#from flask_admin import Admin
from flask_wtf.csrf import CSRFProtect
from flask_googlecharts import GoogleCharts

bootstrap=Bootstrap()

mail=Mail()
db=SQLAlchemy()
# csrf=CSRFProtect()
sess=Session()
charts=GoogleCharts()
#admin=Admin()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_message = 'You Must Login to Access This Page!'
login_manager.login_message_category = 'info'
login_manager.login_view = 'auth.login'

def create_app(config_name=None):
    '''Create all the blue prints and everything'''
    if not config_name:
        config_name=os.environ.get('FLASK_CONFIG','development')
        
    print(config_name)
    app = Flask(__name__)

    app.config.from_object(config[config_name]) #config dict
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)


    # csrf.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)
    app.config["SESSION_SQLALCHEMY"]=db
    sess.init_app(app)
    #sess.app.session_interface.db.create_all()
    charts.init_app(app)


    from .Modules.home import viewhome
    app.register_blueprint(viewhome, template_folder='templates')

    from .Modules.Auth import auth
    app.register_blueprint(auth, template_folder='templates')

    from .Modules.Admin import admin
    app.register_blueprint(admin)

    from .Modules.Question import question
    app.register_blueprint(question, template_folder='templates')

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.globals.update(create_hashid=create_hashid)
    app.jinja_env.globals.update(charts=charts)
    #global error  handler


    @app.errorhandler(404)
    def pg_not_found(e):
        return render_template(template_name_or_list='error/404.html'),404

    #from .Modules.Admin.views import init_admin

    #init_admin(f_admin)
    #admin.init_app(app)



    # print(app.url_map)
    #print(app.extensions)
    return app
