# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, current_app, flash
from flask_login import login_required, current_user
from flask_babelex import gettext

from app.models import Site
from ..utils import Master
from . import admin

@admin.before_request
@login_required
def before_request():
    if not current_user.is_setting:
        current_app.logger.debug('request endpoint: %s' % request.endpoint[6:10])
        if request.path[:8] != '/static/' and request.endpoint[6:10] != 'site':

            flash(gettext('Sorry, please set up the site information first！'), 'danger')

            return redirect(url_for('admin.site'))


@admin.context_processor
def include_common_data():
    """注入共用的变量"""
    # 所属的官网
    current_site = Site.current_site(master_uid=Master.master_uid())

    return {
        'current_site': current_site,
        'site_languages': current_site.languages
    }


@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/help')
@login_required
def help():
    pass