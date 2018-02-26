import os
#
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY =b'r*7\x9aH\x81\xca\x18\xe7\x0f\xc5\x02\xd0\x8c?\t\xae\xea\x83W\x015\x13\xa8G\xfby\xb6'


    WTF_CSRF_SECRET_KEY =b'\xba\xfa\x11_\xb0\xcb\x10Cns\x1e_y\xe4\x01\xe2\xf1\xe0\x82\xea\x17\xc7\xda\x08m-f\xe4'
    #WTF_CSRF_ENABLED=True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #SERVER_NAME='fmsapp.com:5000'
    # SERVER_NAME='localhost:5000'
    # print(SERVER_NAME)

    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_SUBJECT_PREFIX = '[OSFapp]'
    MAIL_SENDER = 'Osfapp Admin <lmnography@gmail.com>'
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')



    SESSION_SQLALCHEMY_TABLE='sessions'

    SESSION_TYPE='sqlalchemy'
    #SESSION_COOKIE_SECURE=True
    PERMANENT_SESSION_LIFETIME=7200
    # SQLALCHEMY_ECHO=True

    ADMIN_EMAIL='leon9923@gmail.com'
    REMEMBER_COOKIE_HTTPONLY=True
    SESSION_COOKIE_HTTPONLY = True
    @staticmethod
    def init_app(app):
        pass



class DevConfig(Config):

    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "devdb.sqlite")
    SQLALCHEMY_DATABASE_URI = 'postgresql://leon:@ll0wfmsapp#@localhost/fmsapp'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://fmsuser:@ll0wfms@localhost/fmsuser'
    TEMPLATES_AUTO_RELOAD=True




class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "testdb.sqlite")


class ProdConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'postgresql://leon:@ll0wfmsapp#@localhost/fmsapp'
    SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir, "prodb.sqlite")
    DEBUG = False


config = {'testing': TestConfig,
'development': DevConfig,
'production': ProdConfig
}
