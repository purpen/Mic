# -*- coding: utf-8 -*-
from flask import url_for
from datetime import datetime
from app import db
from app.models import User
from app.exceptions import ValidationError

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	body = db.Column(db.Text)
	created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	# User一对多关系
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	@staticmethod
	def generate_fake(count=100):
		from random import seed, randint
		import forgery_py

		seed()
		user_count = User.query.count()
		for i in range(count):
			u = User.query.offset(randint(0, user_count - 1)).first()
			p = Post(title=forgery_py.lorem_ipsum.title(),body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
					 created_at=forgery_py.date.date(True),
					 author=u)
			db.session.add(p)
			db.session.commit()

	# 提供的资源没必要和数据库模型的内部表示完全一致
	def to_json(self):
		"""资源和JSON的序列化转换"""
		json_post = {
			'url': url_for('api.get_post', id=self.id, _external=True),
			'body': self.body,
			'created_at': self.created_at,
			'author': url_for('api.get_user', id=self.author_id, _external=True)
		}
		return json_post

	@staticmethod
	def from_json(json_post):
		"""从JSON 格式数据创建"""
		body = json_post.get('body')
		if body is None or body == '':
			raise ValidationError('Post does not have a body')
		return Post(body=body)

	def __repr__(self):
		return '<Post %r>' % self.title