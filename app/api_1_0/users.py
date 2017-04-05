# -*- coding: utf-8 -*-

from . import api

@api.route('/users')
def user():
	return 'This is api.'

@api.route('/users/<int:id>')
def get_user(id):
	"""
	@api {get} /users/:id   Get an user
	@apiVersion 1.0.0
	@apiName get_user
	@apiGroup User

	@apiDescription Gets an user for the given id.

	@apiParam {Number} id    The user's id.

    @apiSuccessExample {json} Success-Response:
    	HTTP/1.1 200 OK
    	{
    		"id": 4812,
    		"username": "MIC"
    	}
	@apiErrorExample {json} Error-Response:
		HTTP/1.1 404 Not Found
		{
			"error": "User Not Found"
		}
	"""
	pass

@api.route('/users/<id>', methods=['POST'])
def update_user():
	"""
	@api {post} /users/:id Update a user
	@apiVersion 1.0.0
	@apiName update_user
	@apiGroup User

	@apiParam {Number} id   The user's id.
	@apiParam {String} first_name The first name of the User.
	@apiParam {String} last_name The last name of the User.
	"""
	return