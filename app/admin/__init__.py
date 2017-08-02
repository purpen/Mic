# -*- coding: utf-8 -*-

from flask import Blueprint, g
from flask_login import current_user

admin = Blueprint('admin', __name__)

from . import dashboard, account, posts, products, brands, categories, settings, file_manager, uploads


# 针对程序全局请求的钩子，
# 必须使用before_app_request修饰器
@admin.before_request
def before_request():
    pass