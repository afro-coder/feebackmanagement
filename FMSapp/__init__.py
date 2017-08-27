from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,url_for
import os

bootstrap=Bootstrap()
db=SQLAlchemy()

def create_app(config_name=None):
    '''Create all the blue prints and everything'''
    if not config_name:
        config_name=os.environ.get('FLASK_CONFIG','development')

    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


    bootstrap.init_app(app)
    db.init_app(app)
    

    from .Modules.home import viewhome
    from .Modules.Auth import auth

    app.register_blueprint(viewhome, template_folder='templates')
    app.register_blueprint(auth, template_folder='templates')

    #global error  handler
    @app.errorhandler(404)
    def pg_not_found(e):
        return render_template(template_name_or_list='error/404.html'),404


    return app
