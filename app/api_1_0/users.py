# -*- coding: utf-8 -*-

from . import api

@api.route('/users')
def user():
	return 'This is api.'

@api.route('/users/<int:id>')
def get_user(id):
	pass