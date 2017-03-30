# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from .forms import LoginForm, RegisterationForm
from . import auth
from ..email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('web.index'))
		flash('Invalid username or password.')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('web.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		db.session.commit()

		# Send confirm.txt email
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm Your Account',
				   'auth/email/confirm', user=user, token=token)
		flash('A confirmation email has been sent to you by email.')
		return redirect(url_for('web.index'))
	return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	"""确认用户账户"""
	if current_user.confirmed:
		return redirect(url_for('web.index'))
	if current_user.confirm(token):
		flash('You have confirmed your account. Thanks!')
	else:
		flash('The confirmation link is invalid or has expired.')
	return redirect(url_for('web.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
	"""重新发送账户确认邮件"""
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirm Your Account',
			   'auth/email/confirm', user=current_user, token=token)
	flash('A new confirmation email has been sent to you by email.')
	return redirect(url_for('web.index'))


# 针对程序全局请求的钩子，必须使用before_app_request修饰器
@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		# 每次收到用户的请求时都要调用ping()方法
		current_user.ping()
		if not current_user.confirmed \
			and request.endpoint[:5] != 'auth.':
			return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('web.index'))
	return render_template('auth/unconfirmed.html')
