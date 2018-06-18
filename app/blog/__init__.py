# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-06-15 10:07:38
# @Last Modified by:   King kaki
# @Last Modified time: 2018-06-15 19:32:50
from flask import Blueprint

blog = Blueprint('blog', __name__)

import app.blog.views
