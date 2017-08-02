# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, current_app, flash
from flask_login import login_required, current_user
from flask_babelex import gettext

from app.models import Site
from ..utils import Master
from . import admin


@admin.before_request
def before_request():
    if not current_user.is_setting:
        current_app.logger.debug('request endpoint: %s' % request.endpoint[6:11])
        if request.path[:8] != '/static/' and request.endpoint[6:11] != 'store':

            flash(gettext('Sorry, please set up the site information first！'), 'danger')

            return redirect(url_for('admin.store'))

@admin.context_processor
def include_common_data():
    """注入共用的变量"""
    # 所属的官网
    current_site = Site.query.filter_by(master_uid=Master.master_uid()).first()

    return {
        'current_site': current_site
    }


@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')

@admin.route('/help')
def help():
    pass