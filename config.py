# -*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~~~~~~~~~

    Default configuration

    :copyright: (c) 2017 by Mic.
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# available languages
LANGUAGES = {
    'zh': 'Chinese',
    'en': 'English',
}

class Config:

    # change this in your production settings !!!
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Aine#2018%0110!'

    # 默认语言
    BABEL_DEFAULT_LOCALE = 'zh'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

    # 配置输出SQL语句
    SQLALCHEMY_ECHO = True

    # 每次request自动提交db.session.commit()
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # slow database query threshold (in seconds)
    DATABASE_QUERY_TIMEOUT = 0.5

    # 管理员
    ADMINS = ('admin@qq.com')

    # 邮件服务
    DEFAULT_MAIL_SENDER = 'support@qq.com'

    MAIL_SERVER = 'stmp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'Admin'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Mic2018'
    MAIL_SUBJECT_PREFIX = '[MIC]'
    MAIL_SENDER = os.environ.get('MAIL_SENDER') or DEFAULT_MAIL_SENDER

    # 日志
    DEBUG_LOG = 'logs/urk-debug.log'
    ERROR_LOG = 'logs/urk-error.log'

    # pagination
    MAX_SEARCH_RESULTS = 50
    POSTS_PER_PAGE = 50

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    # Examples: mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Urk426#Db10@localhost/micdaba_dev'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Urk426#Db10@localhost/micdaba_test'

class ProductionConfig(Config):
    DEBUG_LOG = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Urk426#Db10@localhost/micdataz'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}