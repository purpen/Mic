# -*- coding: utf-8 -*-

import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
	def test_password_setter(self):
		u = User(password='cat')
		self.assertTrue(u.password_hash is not None)

	def test_no_password_getter(self):
		u = User(password='cat')
		with self.assertRaises(AttributeError):
			u.password

	def test_password_verification(self):
		user = User(password='cat')
		self.assertTrue(user.verify_password('cat'))
		self.assertFalse(user.verify_password('dog'))