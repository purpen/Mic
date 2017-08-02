# -*- coding: utf-8 -*-
from flask import g, current_app, render_template, session, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_babelex import gettext
from .. import db
from . import web
from .forms import SetupForm
from app.models import User, Site

@web.route('/')
# @user_has('create_users')
def index():
    current_app.logger.debug('login user: %s' % current_user)
    return render_template('web/index.html',
                           language=current_app.config['BABEL_DEFAULT_LOCALE']
                           )

@web.route('/store/setup', methods=['GET', 'POST'])
def setup():
    """一键开通"""
    form = SetupForm()
    if form.validate_on_submit():
        # 1、注册账号
        user = User(email=form.email.data,
                    password=form.password.data,
                    username=form.email.data,
                    time_zone='zh')
        db.session.add(user)

        # 2、开通官网
        site = Site(
            master_uid = user.id,
            serial_no = Site.make_unique_serial_no(),
            name = form.store_name.data
        )
        db.session.add(site)

        db.session.commit()

        # 3、自动登录
        login_user(user)

        flash(gettext('Setup store is Ok!'), 'success')

        return redirect(url_for('admin.index'))

    return render_template('web/setup.html',
                           form=form)

