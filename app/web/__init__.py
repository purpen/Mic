# -*- coding: utf-8 -*-

from flask import Blueprint

web = Blueprint('web', __name__)

from . import views, user