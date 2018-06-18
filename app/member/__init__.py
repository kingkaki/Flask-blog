# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-06-15 09:56:46
# @Last Modified by:   King kaki
# @Last Modified time: 2018-06-15 19:32:21
from flask import Blueprint

member = Blueprint('member', __name__)

import app.member.views