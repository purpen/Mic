# -*- coding: utf-8 -*-

from flask import render_template, session, redirect, url_for, flash
from app.models import Category
from . import web

@web.route('/')
def index():
	cate = Category.query.all()
	return render_template('web/index.html')