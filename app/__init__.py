# -*- coding: utf-8 -*-
"""
	__init__.py
	~~~~~~~~~~~~~~

	:copyright: (c) 2017 by mic.
"""

from flask import Flask
# 脚本化管理
from flask_script import Manager, Shell
# 装载静态文件
from flask_bootstrap import Bootstrap, WebCDN
# 本地化日期和时间
from flask_moment import Moment
# 邮件
from flask_mail import Mail
# 数据库连接
from flask_sqlalchemy import SQLAlchemy
# 管理用户认证系统中的认证状态
from flask_login import LoginManager, current_user
# 国际化和本地化
from flask_babelex import Babel
from flask_pjax import PJAX
# 导入上传
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf.csrf import CSRFProtect

# 导入配置参数
from config import config


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()
babel = Babel()
pjax = PJAX()
# 创建set
uploader = UploadSet('photos', IMAGES)
csrf = CSRFProtect()

# Flask-Login初始化
login_manager = LoginManager()
# 属性可以设为None、'basic' 或'strong'
login_manager.session_protection = 'strong'
# 设置登录页面的端点
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    babel.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    pjax.init_app(app)
    csrf.init_app(app)


    # 初始化
    configure_uploads(app, uploader)
    # 文件大小限制，默认为16MB
    patch_request_class(app)

    # logging setting
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(app.config['ERROR_LOG'])
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Urk startup')

    # attach routes

    from .main import main
    app.register_blueprint(main)

    from .web import web
    app.register_blueprint(web)

    from .admin import admin
    app.register_blueprint(admin, url_prefix='/admin')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    # API REST
    from .api_1_0 import api as api_1_0
    app.register_blueprint(api_1_0, url_prefix='/api/v1.0')

    from .blog import blog
    app.register_blueprint(blog)

    # 附加路由和自定义的错误页面

    app.extensions['bootstrap']['cdns']['jquery'] = WebCDN(
        '//cdn.bootcss.com/jquery/3.2.1/'
    )

    app.extensions['bootstrap']['cdns']['bootstrap'] = WebCDN(
        '//cdn.bootcss.com/bootstrap/3.3.7/'
    )

    from .main.filters import timestamp2string, short_filename, supress_none
    app.add_template_filter(timestamp2string, 'timestamp2string')
    app.add_template_filter(short_filename, 'short_filename')
    app.add_template_filter(supress_none, 'supress_none')

    return app