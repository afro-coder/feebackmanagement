
import os
#
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY ="Add secret key here"

    WTF_CSRF_SECRET_KEY ="Add wtf secret"
    HASH_KEY=os.urandom(28).hex()
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER='smtphost'
    MAIL_PORT="int(Port)"
    MAIL_USE_TLS=True
    MAIL_SUBJECT_PREFIX = ''
    MAIL_SENDER = "AdminEmail"
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')



    SESSION_SQLALCHEMY_TABLE='sessions'

    SESSION_TYPE='sqlalchemy'
    #SESSION_COOKIE_SECURE=True
    PERMANENT_SESSION_LIFETIME=7200
    #Enable if you want queries to be printed
    # SQLALCHEMY_ECHO=True

    ADMIN_EMAIL=''
    REMEMBER_COOKIE_HTTPONLY=True
    SESSION_COOKIE_HTTPONLY = True
    @staticmethod
    def init_app(app):
        pass



class DevConfig(Config):

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "devdb.sqlite")
    TEMPLATES_AUTO_RELOAD=True




class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "testdb.sqlite")


class ProdConfig(Config):

    SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir, "prodb.sqlite")
    DEBUG = False


config = {'testing': TestConfig,
'development': DevConfig,
'production': ProdConfig
}
