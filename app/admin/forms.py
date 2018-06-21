# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-06-15 09:56:18
# @Last Modified by:   King kaki
# @Last Modified time: 2018-06-21 14:33:59
from wtforms import Form, BooleanField, TextField, PasswordField, IntegerField,validators
from wtforms.validators import DataRequired, ValidationError
from app.models import *
from flask import session, abort

class LoginForm(Form):
	username = TextField('username', [validators.Required()])
	password = PasswordField('password', [validators.Required()])

	def validate_username(self, field):
		user = Admin.query.filter_by(username=field.data).count()
		if user == 0:
			raise ValidationError("username does not exist.")


class PasswordForm(Form):
	oldpassword = PasswordField('oldpassword')
	newpassword = PasswordField('newpassword', [
		validators.Required(),
		validators.EqualTo('password_confirm', message='Passwords must match')
	])
	password_confirm = PasswordField('password_confirm')