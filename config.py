import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY =b"'\x85|\xc9R\x99\xa8\x15h\x88\xd2\x13a\x06\xba\x7f\xe3\xb6Ep\xd4\xab\xf8\x91\x1b\xb6XX"

    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    WTF_CSRF_SECRET_KEY =b'R\x1e\xdbeV[\xb7\xc8\xbd?\xce\x06\x1c\x08\x1a\xd9-\x8diu\x03`\x88_\x00t\xc1\xbd'


    #SQLALCHEMY_DATABASE_URI = 'sqlite:////:' + os.path.join(basedir, "devdb.db")

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "devdb.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
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
