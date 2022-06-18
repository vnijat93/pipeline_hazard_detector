from os import path

basedir = path.abspath(path.dirname(__file__))


class Config:

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    DEBUG = True


config = {
    "dev": DevelopmentConfig,
    "default": DevelopmentConfig
}
