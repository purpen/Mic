# -*- coding: utf-8 -*-

from flask import g, current_app, render_template, session, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_babelex import gettext
from . import web
from ..decorators import user_has, user_is

@web.route('/')
@login_required
@user_has('create_users')
def index():
    return render_template('web/index.html', language=current_app.config['BABEL_DEFAULT_LOCALE'])