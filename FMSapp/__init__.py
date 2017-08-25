from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


bootstrap=Bootstrap()
db=SQLAlchemy()
def create_app(config_name):
    '''Create all the blue prints and everything'''
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    
    bootstrap.init_app(app)
    db.init_app(app)




    #from .Modules.Auth.Login import login

    from .Modules.home import viewhome
    from .Modules.Auth import auth



    app.register_blueprint(viewhome, template_folder='templates')
    app.register_blueprint(auth, template_folder='templates')
    return app
