# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-06-15 09:55:30
# @Last Modified by:   King kaki
# @Last Modified time: 2018-06-19 13:01:17

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@127.0.0.1/flask-blog"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'cc1df2e4-fd25-4a33-a7ae-9555f5e361b0'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__),'static','img')
app.debug = True
db = SQLAlchemy(app)

from app.member import member
from app.admin import admin
from app.blog import blog

app.register_blueprint(member, url_prefix='/member')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(blog, url_prefix='/')


@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404