# -*- coding: utf-8 -*-

from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required
from . import admin

@admin.route('/')
@login_required
def postlist():
	return render_template('admin/posts/list.html')