# -*- coding: utf-8 -*-
from flask import render_template

from . import admin


@admin.route('/profile')
def profile():
    pass

@admin.route('/settings')
def settings():
    pass