# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-06-15 09:56:08
# @Last Modified by:   King kaki
# @Last Modified time: 2018-06-15 13:50:10

from flask import Blueprint

admin = Blueprint('admin', __name__)

import app.admin.views