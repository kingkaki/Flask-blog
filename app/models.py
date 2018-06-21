# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-06-15 10:19:36
# @Last Modified by:   King kaki
# @Last Modified time: 2018-06-21 12:10:43

from datetime import datetime

from . import db
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask, render_template
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@127.0.0.1/flask-blog"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)


class Member(db.Model):
	__tablename__ = "member"
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50)) 
	password = db.Column(db.String(255)) 
	realname = db.Column(db.String(50)) 
	email = db.Column(db.String(50)) 
	phone = db.Column(db.String(11)) 
	address = db.Column(db.String(100))
	avatar = db.Column(db.String(255))
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)
	signature = db.Column(db.Text)
	articles = db.relationship('Article', backref='Member') #外键关联
	comments = db.relationship('Comment', backref='Member') 
	userlogs = db.relationship('Userlog', backref='Member') 

	def __repr__(self):
		return "<User %r>" % self.username

	def check_pwd(self, password):
		from werkzeug.security import check_password_hash
		return check_password_hash(self.password, password)

class Userlog(db.Model):
	__tablename__ = 'userlog'
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('member.id'))
	ip = db.Column(db.String(50)) 
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)

	def __repr__(self):
		return "<Userlog %r>" % self.id


class Article(db.Model):
	__tablename__ = "article"
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('member.id'))
	title = db.Column(db.String(255)) 
	content = db.Column(db.Text())
	click_num = db.Column(db.Integer, default=0)
	addtime = db.Column(db.DateTime, index=True,)
	last_modify = db.Column(db.DateTime, index=True, default=datetime.now)
	comments = db.relationship('Comment', backref='Article')

	def __repr__(self):
		return "<Article %r>" % self.title

class Comment(db.Model):
	__tablename__ = "comment"
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('member.id'))
	article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
	content = db.Column(db.Text())
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)

	def __repr__(self):
		return "<Comment %r by %r>" % (self.id, self.user_id) 

#管理员
class Admin(db.Model):
	__tablename__ = 'admin'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50)) 
	password = db.Column(db.String(255)) 
	is_super = db.Column(db.Boolean, default=False)	
	realname = db.Column(db.String(50)) 
	email = db.Column(db.String(50)) 
	phone = db.Column(db.String(11)) 
	address = db.Column(db.String(100))
	avatar = db.Column(db.String(255))
	signature = db.Column(db.Text)
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)
	adminlogs = db.relationship('Adminlog', backref='Admin') 

	def __repr__(self):
		return "<Admin %r>" % (self.username) 

	def check_pwd(self, password):
		from werkzeug.security import check_password_hash
		return check_password_hash(self.password, password)


class Adminlog(db.Model):
	__tablename__ = 'adminlog'
	id = db.Column(db.Integer, primary_key = True)
	admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
	ip = db.Column(db.String(50)) 
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)

	def __repr__(self):
		return "<Adminlog %r>" % self.id


if __name__ == '__main__':
	db.create_all()
	# from werkzeug.security import generate_password_hash
	# admin = Member(
	# 	username = 'kingkk',
	# 	password = generate_password_hash('kingkk'),
	# 	is_super = True

	# 	)

	# db.session.add(admin)
	# db.session.commit()