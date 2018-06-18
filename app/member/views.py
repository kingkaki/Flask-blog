# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-06-15 09:57:04
# @Last Modified by:   King kaki
# @Last Modified time: 2018-06-18 16:28:15
import functools
from datetime import datetime
from . import member
from flask import render_template, redirect, url_for, session, flash, request
from werkzeug.security import check_password_hash, generate_password_hash
from app.member.forms import *
from app.models import Member, Article, Comment
from app import db


def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if session.get('user') is None:
			return redirect(url_for('member.login', next= request.url))
		return view(**kwargs)
	return wrapped_view



@member.route('/')
@login_required
def index():
	return render_template('member/index.html')



@member.route('/register', methods=('GET','POST'))
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate():
			user = Member(
				username = form.username.data,
				email = form.email.data,
				password = generate_password_hash(form.password.data)
			)
			db.session.add(user)
			db.session.commit()
			return redirect(request.args.get('next') or url_for( 'member.login'))

		else:
			flash('may username already exists.')
	return render_template('member/register.html', form=form)



@member.route('/login', methods=('GET', 'POST'))
def login():
	form = LoginForm(request.form)

	if request.method == 'POST' :
		if form.validate():
			user = Member.query.filter_by(username=form.data['username']).first()
			if not user.check_pwd(form.data['password']):
				flash("password error.")
				return render_template('member/login.html')
			session['user'] = user.id
			return redirect(request.args.get('next') or url_for('member.index'))
		else:
			flash('username does not exist.')
		
	return render_template('member/login.html')



@member.route('/logout')
@login_required
def lougout():
	session.clear()
	return redirect(url_for('member.index'))



@member.route('/create', methods=('GET', 'POST'))
@login_required
def create():
	form = CreateForm(request.form)

	if request.method == 'POST':
		if form.validate():
			print(456)
			article = Article(
				title = form.data['title'],
				content = form.data['content'],
				addtime = datetime.now(),
				user_id = session['user'],
			)
			db.session.add(article)
			a = db.session.commit()
			flash("Create Success.")
			return redirect(url_for('member.index'))
		
		flash("Create Error.")
		return render_template('member/create.html')
	else:
		return render_template('member/create.html')


@member.route('/create', methods=('GET', 'POST'))
@login_required
def update():
	form = UpdateForm(request.form)
	if request



@member.route('/comment', methods=('POST',))
@login_required
def comment():
	form = CommentForm(request.form)
	print(request.form)
	if form.validate():
		comment = Comment(
			user_id = session['user'],
			article_id = form.data['articleid'],
			content = form.data['comment']
		)
		db.session.add(comment)
		db.session.commit()
		flash('Comment Success')

		return redirect('article/'+str(form.data['articleid']))


	else:
		flash('comment error')
		return redirect(url_for('blog.article'))

