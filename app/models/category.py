# -*- coding: utf-8 -*-

from app import db

class Category(db.Model):
	__tablename__ = 'fp_categories'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True, index=True)