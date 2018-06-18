# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-06-15 09:56:55
# @Last Modified by:   King kaki
# @Last Modified time: 2018-06-18 14:06:12
from wtforms import Form, BooleanField, TextField, PasswordField, IntegerField,validators
from wtforms.validators import DataRequired, ValidationError
from app.models import Member, Article



class RegisterForm(Form):
	username = TextField('username', [validators.Required()])
	email = TextField('email', [validators.Email()])
	password = PasswordField('password', [
		validators.Required(),
		validators.EqualTo('password_confirm', message='Passwords must match')
	])
	password_confirm = PasswordField('password_confirm')

	def validate_username(self, field):
		user = Member.query.filter_by(username=field.data).count()
		if user > 0:
			raise ValidationError("username already exists.")


class LoginForm(Form):
	username = TextField('username', [validators.Required()])
	password = PasswordField('password', [validators.Required()])

	def validate_username(self, field):
		user = Member.query.filter_by(username=field.data).count()
		if user == 0:
			raise ValidationError("username does not exist.")


class CreateForm(Form):
	title = TextField('title', [validators.Required()])
	content  = TextField('content',[validators.length(min=10)])

class CommentForm(Form):
	comment = TextField('title', [validators.Required()])
	articleid = IntegerField('articleid')

	def validate_articleid(self, field):
		article = Article.query.filter_by(id=field.data).count()
		if article == 0:
			raise ValidationError("article does not exist.")
