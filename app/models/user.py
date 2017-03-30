# -*- coding: utf-8 -*-
from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)

	def __repr__(self):
		return '<Role %r>' % self.name

class Follow(db.Model):
	__tablename__ = 'follows'
	follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
							primary_key=True)
	followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
							primary_key=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	confirmed = db.Column(db.Boolean, default=False)

	# 真实资料信息
	name = db.Column(db.String(64))
	location = db.Column(db.String(64))
	about_me = db.Column(db.Text())
	member_since = db.Column(db.DateTime(), default=datetime.utcnow)
	last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

	# 博客文章一对多关系
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	# 一对多关系
	# lazy 模式可以实现立即从联结查询中加载相关对象
	# db.backref() 参数并不是指定这两个关系之间的引用关系，而是回引Follow 模型
	followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
							   backref=db.backref('follower', lazy='joined'),
							   lazy='dynamic',
							   cascade='all, delete-orphan')

	followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
								backref=db.backref('followed', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)

		# 自动设置自己关注自己
		self.follow(self)



	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def generate_confirmation_token(self, expiration=3600):
		"""生成一个令牌，有效期默认为一小时."""
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id})

	def confirm(self, token):
		"""检验令牌，如果检验通过，则把新添加的confirmed 属性设为True."""
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False

		if data.get('confirm') != self.id:
			return False

		self.confirmed = True
		db.session.add(self)
		db.session.commit()
		return True

	def ping(self):
		"""每次收到用户的请求时都要调用ping()方法"""
		self.last_seen = datetime.utcnow()
		db.session.add(self)

	# API基于令牌的认证
	def generate_auth_token(self, expiration):
		s = Serializer(current_app.config['SECRET_KEY'],
					   expires_in=expiration)
		return s.dumps({'id': self.id})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return None
		return User.query.get(data['id'])

	@staticmethod
	def generate_fake(count=100):
		"""自动生成测试数据"""
		from sqlalchemy.exc import IntegrityError
		from random import seed
		import forgery_py

		seed()
		for i in range(count):
			u = User(email=forgery_py.internet.email_address(),
					 username=forgery_py.internet.user_name(True),
					 password=forgery_py.lorem_ipsum.word(),
					 confirmed=True,
					 name=forgery_py.name.full_name(),
					 location=forgery_py.address.city(),
					 about_me=forgery_py.lorem_ipsum.sentence(),
					 member_since=forgery_py.date.date(True))
			db.session.add(u)
			try:
				db.session.commit()
			except:
				db.session.rollback()

	# 定义辅助方法
	def follow(self, user):
		if not self.is_following(user):
			f = Follow(follower=self, followed=user)
			db.session.add(f)

	def unfollow(self, user):
		f = self.followed.filter_by(followed_id=user.id)
		if f:
			db.session.add(f)

	def is_following(self, user):
		return self.followed.filter_by(followed_id=user.id).first() is not None

	def is_followed_by(self, user):
		return self.followers.filter_by(follower_id=user.id).first() is not None


	def __repr__(self):
		return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

	def is_administrator(self):
		return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
	"""使用指定的标识符加载用户"""
	return User.query.get(int(user_id))