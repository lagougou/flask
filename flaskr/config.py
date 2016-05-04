import os

basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY='hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <jiangruitc@163.com>'
    FLASKY_ADMIN = "jiangruitc@163.com"

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = "jiangruitc@163.com"
    MAIL_PASSWORD = "jiangrui992716"
    FLASKY_POSTS_PER_PAGE=15
    FLASKY_FOLLOWERS_PER_PAGE=15
    FLASKY_COMMENTS_PER_PAGE=10
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                                'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    Testing=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                            'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls,app):
        Config.init_app(app)

        import logging
        from logging.handlers import SMTPHandler
        credentials=None
        secure=None
        if getattr(cls,'MAIL_USERNAME',None) is not None:
            credentials=(cls.MAIL_USERNAME,cls.MAIL_PASSWORD)
            if getattr(cls,'MAIL_USE_TLS',None):
                secure()
            mail_handler=SMTPHandler(
                mailhost=(cls.MAIL_SERVER,cls.MAIL_PORT),
                fromaddr=cls.FLASKY_MAIL_SENDER,
                toaddrs=[cls.FLASKY_ADMIN],
                subject=cls.FLASKY_MAIL_SUBJECT_PREFIX+'APPLICATION ERROR!',
                credentials=credentials,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)


config={
    "development":DevelopmentConfig,
    "testin5g":TestingConfig,
    "production":ProductionConfig,
    "default":DevelopmentConfig
}



