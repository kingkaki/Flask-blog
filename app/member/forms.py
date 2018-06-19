# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-06-15 09:56:55
# @Last Modified by:   King kaki
# @Last Modified time: 2018-06-19 13:04:55
from wtforms import Form, BooleanField, TextField, PasswordField, IntegerField,validators
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import Member, Article
from flask import session, abort

def get_article(id, check_author=True):
	article = Article.query.get(id)
	author = Member.query.get(article.user_id)

	if article is None:
		abort(404, "Article id {} doesn't exist".format(id))

	if check_author and author.id != session['user']:
		abort(403)

	return article

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

class UpdateForm(Form):
	article_id = IntegerField('article_id')
	title = TextField('title', [validators.Required()])
	content  = TextField('content',[validators.length(min=10)])

	def validate_article_id(self, field):
		article = Article.query.get(field.data)
		if article.user_id != session['user']:
			abort(403)
			
class PasswordForm(Form):
	oldpassword = PasswordField('oldpassword')
	newpassword = PasswordField('newpassword', [
		validators.Required(),
		validators.EqualTo('password_confirm', message='Passwords must match')
	])
	password_confirm = PasswordField('password_confirm')


class ModifiyForm(Form):
	username = TextField('username', [validators.Required()])
	signature = TextField('signature')
	email = TextField('signature', [validators.Email()])
	realname = TextField('realname')
	phone = IntegerField('phone', [validators.NumberRange(10000000000,19999999999)])
	address = TextField('realname')


class AvatarForm(Form):
	avatar = FileField("avatar",validators = [FileAllowed(['jpg','png'],'Images Only!'), FileRequired()])