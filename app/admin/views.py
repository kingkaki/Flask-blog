# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-06-15 09:56:25
# @Last Modified by:   King kaki
# @Last Modified time: 2018-06-15 10:03:58

from . import admin

@admin.route('/')
def index():
	return "hello world!"