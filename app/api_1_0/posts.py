# -*- coding: utf-8 -*-
from flask import g, jsonify, request, url_for
from app.models import Post
from app import db
from . import api
from .authentication import auth
from .errors import forbidden

@api.route('/posts/')
@auth.login_required
def get_posts():
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.paginate(page, per_page=20, error_out=False)
	posts = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('api.get_posts', page=page-1, _external=True)
	next = None
	if pagination.has_next:
		next = url_for('api.get_posts', page=page+1, _external=True)
	return jsonify({
		'posts': [post.to_json() for post in posts],
		'prev': prev,
		'next': next,
		'count': pagination.total
	})

@api.route('/posts/<int:id>')
def get_post(id):
	post = Post.query.get_or_404(id)
	return jsonify(post.to_json)

@api.route('/posts', methods=['POST'])
def new_post():
	post = Post.from_json(request.json)
	post.author = g.current_user
	db.session.add(post)
	db.session.commit()

	return jsonify(post.to_json()), 201, \
		   {'Location': url_for('api.get_post', id=post.id, _external=True)}

@api.route('/posts/<int:id>', methods=['PUT'])
def edit_post(id):
	post = Post.query.get_or_404(id)
	if g.current_user != post.author:
		return forbidden('Insufficient permissions')
	post.body = request.json.get('body', post.body)
	db.session.add(post)
	return jsonify(post.to_json())