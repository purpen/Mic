#!venv/bin/python
# -*- coding: utf-8 -*-
"""
    tr_update.py
    ~~~~~~~~~~~~~

    更新语言目录
    :copyright: (c) 2017 by Mic.
"""

import os, sys

pybabel = 'venv/bin/pybabel'

os.system(pybabel + ' extract -F babel.cfg -k lazy_gettext -o messages.pot app')
os.system(pybabel + ' update -i messages.pot -d app/translations')
os.unlink('messages.pot')