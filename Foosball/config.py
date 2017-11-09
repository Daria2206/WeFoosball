import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY= os.environ.get('SECRET_KEY') or "Hard to guss string"
    USERNAME='admin',
    PASSWORD='default'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'foosball.sqlite')

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig}
