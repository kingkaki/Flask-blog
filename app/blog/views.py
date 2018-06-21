# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-06-15 10:07:47
# @Last Modified by:   King kaki
# @Last Modified time: 2018-06-21 11:06:15
from . import blog
from flask import render_template, redirect, url_for, session, flash, request
from app.models import *

@blog.route('/')
def index():
	articles = Article.query.all()
	return render_template('blog/index.html', articles=articles)


@blog.route('/article/<int:id>')
def article(id):
	article = Article.query.get(id)
	author = Member.query.get(article.user_id)

	click = Article.query.filter_by(id=id).update(dict(click_num = article.click_num+1))
	db.session.commit()
	comments = Comment.query.filter_by(article_id=id).all()
	comments_author=[]
	for comment in comments:
		comments_author.append(Member.query.get(comment.user_id))
	return render_template('blog/article.html', article=article, author=author, comments=comments, comments_author=comments_author)

