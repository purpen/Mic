# -*- coding: utf-8 -*-

from flask import g, current_app, render_template, session, redirect, url_for, flash, request
from flask_babelex import gettext
from . import web

@web.route('/')
def index():
    flash(gettext('Invalid login. Please login again.'))
    return render_template('web/index.html', language=current_app.config['BABEL_DEFAULT_LOCALE'])