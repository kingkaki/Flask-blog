# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-06-15 09:56:25
# @Last Modified by:   King kaki
# @Last Modified time: 2018-06-21 16:05:04

import functools
from . import admin

from flask import render_template, redirect, url_for, session, flash, request
from app.admin.forms import *
from app.models import *
from werkzeug import generate_password_hash

def admin_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if session.get('admin') is None:
			return redirect(url_for('admin.login', next= request.url))
		return view(**kwargs)
	return wrapped_view



@admin.route('/')
@admin_required
def index():
	admin = Admin.query.get(session['admin'])
	return render_template('admin/index.html', admin = admin)


@admin.route('/login', methods=('GET', 'POST'))
def login():
	form = LoginForm(request.form)


	if request.method == 'POST' :
		if form.validate():
			admin = Admin.query.filter_by(username=form.data['username']).first()
			if not admin.check_pwd(form.data['password']):
				flash("password error.")
				return render_template('admin/login.html')
			session['admin'] = admin.id
			adminlog = Adminlog(
				admin_id = admin.id,
				ip = request.remote_addr
			)
			db.session.add(adminlog)
			db.session.commit()
			return redirect(request.args.get('next') or url_for('admin.index'))
		else:
			flash('username does not exist.')
		
	return render_template('admin/login.html')

@admin.route('/adminlog')
@admin_required
def adminlog():
	adminlogs = Adminlog.query.all()
	admin = Admin.query.get(session['admin'])
	adminnames = [ (Admin.query.get(admin.admin_id)).username  for admin in adminlogs ]
	for i in range(len(adminlogs)):
		adminlogs[i].name = adminnames[i]
	return render_template('admin/adminlog.html', admin=admin, adminlogs=adminlogs)


@admin.route('/password', methods=('POST','GET'))
@admin_required
def password():
	admin = Admin.query.get(session['admin'])
	form = PasswordForm(request.form)

	if request.method == 'POST':
		if form.validate():
			if admin.check_pwd(form.data['oldpassword']):
				admin = Admin.query.filter_by(id=session['admin']).update(
					dict( password = generate_password_hash(form.data['newpassword'])))
				db.session.commit()
				return redirect(url_for('admin.login'))
			else:
				flash('Old Password Error.')
		else:
			flash('May Passwords not match.')
	return render_template('admin/password.html', admin=admin)

@admin.route('/article', methods=('POST','GET'))
@admin_required
def article():
	articles = Article.query.all()
	authornames = [ (Member.query.get(article.user_id)).username  for article in articles ]
	commenttime =  [ Comment.query.filter_by(article_id=article.id).count() for article in articles ]
	for i in range(len(articles)):
		articles[i].author = authornames[i]
		articles[i].commenttime = commenttime[i]
	return render_template('admin/article.html', articles=articles)


@admin.route('/delete/<int:id>', methods=('POST',))
@admin_required
def delete(id):
	article = Article.query.get(id)
	db.session.delete(article)
	db.session.commit()
	return redirect( request.args.get('next') or 'admin.article' )

@admin.route('/user')
@admin_required
def user():
	members = Member.query.all() 
	admins = Admin.query.all()
	users = []
	for admin in admins:
		users.append(admin)
	for member in members:
		users.append(member)
	return render_template('admin/user.html', users = users)