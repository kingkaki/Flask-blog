# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-06-15 09:57:04
# @Last Modified by:   King kaki
# @Last Modified time: 2018-06-19 14:24:23
import functools
import os
from datetime import datetime
from . import member
from flask import render_template, redirect, url_for, session, flash, request
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from app.member.forms import *
from app.models import Member, Article, Comment, Userlog
from app import db, app


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
	user = Member.query.get(session['user'])

	return render_template('member/index.html', user=user)



@member.route('/register', methods=('GET','POST'))
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate():
			user = Member(
				username = form.username.data,
				email = form.email.data,
				password = generate_password_hash(form.password.data),
				avatar = url_for('static', filename='img/avatars/default.jpg')
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
			userlog = Userlog(
				user_id = user.id,
				ip = request.remote_addr
			)
			db.session.add(userlog)
			db.session.commit()
			return redirect(request.args.get('next') or url_for('member.index'))
		else:
			flash('username does not exist.')
		
	return render_template('member/login.html')



@member.route('/logout')
@login_required
def logout():
	session.clear()
	return redirect(url_for('member.index'))



@member.route('/create', methods=('GET', 'POST'))
@login_required
def create():
	form = CreateForm(request.form)

	if request.method == 'POST':
		if form.validate():
			article = Article(
				title = form.data['title'],
				content = form.data['content'],
				addtime = datetime.now(),
				user_id = session['user'],
			)
			db.session.add(article)
			a = db.session.commit()
			return redirect(url_for('member.index'))
		
		flash("Create Error.")
		return render_template('member/create.html')
	else:
		return render_template('member/create.html')


@member.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
	form = UpdateForm(request.form)
	# print(request.form)
	if request.method == 'POST' and form.validate():
		article = Article.query.filter_by(id=form.data['article_id']).update(
			dict(
				title = form.data['title'],
				content = form.data['content'],
				last_modify = datetime.now()
			)
		)
		db.session.commit()
		new_article = get_article(id)
		return render_template('member/update.html', article=new_article)
	else:
		article = get_article(id)
		return render_template('member/update.html', article=article)



@member.route('/comment', methods=('POST',))
@login_required
def comment():
	form = CommentForm(request.form)
	if form.validate():
		comment = Comment(
			user_id = session['user'],
			article_id = form.data['articleid'],
			content = form.data['comment']
		)
		db.session.add(comment)
		db.session.commit()
		return redirect('article/'+str(form.data['articleid']))


	else:
		flash('comment error')
		return redirect(url_for('blog.article'))

@member.route('/modify', methods=('POST','GET'))
@login_required
def modify():
	form = ModifiyForm(request.form)

	if request.method == 'POST':
		if form.validate():
			user = Member.query.filter_by(id=session['user']).update(
				dict(
					username = form.data['username'],
					signature = form.data['signature'],
					email = form.data['email'],
					realname = form.data['realname'],
					phone = form.data['phone'],
					address = form.data['address'],
				)
			)
			db.session.commit()

		else:
			flash('Incorrect Format.')
	user = Member.query.get(session['user'])

	return render_template('member/modify.html', user=user)


@member.route('/password', methods=('POST','GET'))
@login_required
def password():
	user = Member.query.get(session['user'])
	form = PasswordForm(request.form)
	# print(request.form)
	if request.method== 'POST':
		if form.validate():
			if check_password_hash(user.password, form.data['oldpassword']):

				user = Member.query.filter_by(id=session['user']).update(
					dict( password = generate_password_hash(form.data['newpassword'])))
				db.session.commit()
				return redirect(url_for('member.login'))
			else:
				flash('Old Password Error.')
		else:
			flash('May Passwords not match.')

	return render_template('member/password.html', user=user)


@member.route('/articles')
@login_required
def articles():
	articles = Article.query.filter_by(user_id = session['user']).all()
	return render_template('member/articles.html', articles=articles)


@member.route('/avatar', methods=('POST',))
@login_required
def avatar():
	form = AvatarForm(request.files)
	if form.validate():
		import hashlib
		avatar = form.avatar.data
		filename = secure_filename(avatar.filename)

		ext = os.path.splitext(filename)[1]  #取后缀		
		filename = hashlib.md5(avatar.read()).hexdigest()+ext  #文件哈希
		avatar.seek(0)  #指针重回起点

		file_path = os.path.join(app.config['UPLOAD_FOLDER'],'avatars', filename)
		avatar.save(file_path)


		user = Member.query.filter_by(id=session['user']).update(
			dict(avatar = '/static/img/avatars/'+filename))
		db.session.commit()		

	return redirect(url_for('member.modify'))


@member.route('/userlog')
@login_required
def userlog():
	userlogs = Userlog.query.filter_by(user_id=session['user']).all()
	user = Member.query.get(session['user'])
	return render_template('member/userlog.html', userlogs=userlogs, user=user)



