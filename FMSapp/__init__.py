from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,url_for,session
import os
from flask_login import LoginManager
from flask_sessionstore import Session
from flask_mail import Mail
bootstrap=Bootstrap()

sess=Session()
mail=Mail()
db=SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name=None):
    '''Create all the blue prints and everything'''
    if not config_name:
        config_name=os.environ.get('FLASK_CONFIG','development')

    app = Flask(__name__)

    app.config.from_object(config[config_name]) #config dict
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    sess.init_app(app)
    #sess.app.session_interface.db.create_all()
    login_manager.init_app(app)

    from .Modules.home import viewhome
    app.register_blueprint(viewhome, template_folder='templates')
    from .Modules.Auth import auth
    app.register_blueprint(auth, template_folder='templates')
    from .Modules.Admin import admin
    app.register_blueprint(admin, template_folder='templates')

    from .Modules.Question import question
    app.register_blueprint(question, template_folder='templates')

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    #global error  handler
    @app.errorhandler(404)
    def pg_not_found(e):
        return render_template(template_name_or_list='error/404.html'),404


    return app
