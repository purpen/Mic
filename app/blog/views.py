# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from app import db
from app.models import Post
from .forms import PostForm
from . import blog

@blog.route('/')
def index():
	page = request.args.get('page', 1, type=int)

	pagination = Post.query.order_by(Post.created_at.desc()).paginate(
		page, per_page=15, error_out=False)
	posts = pagination.items
	return render_template('blog/index.html',
						   posts=posts,
						   pagination=pagination)

@blog.route('/post/<int:id>')
def post(id):
	"""显示文章详情"""
	post = Post.query.get_or_404(id)
	return render_template('blog/post.html', post=post)

@blog.route('/edit_post', methods=['GET', 'POST'])
def edit_post():
	"""新建或编辑博客文字"""
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.body.data,
					author=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('.index'))
	return render_template('blog/edit_post.html', form=form)