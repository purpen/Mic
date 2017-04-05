# -*- coding: utf-8 -*-
import urllib, httplib, json
from flask import current_app
from flask_babelex import gettext


def google_translate(text, source_lang, dest_lang):
    if not current_app.config['DEBUG']:
        return gettext('Error: translation service not available.')
    try:
        params = urllib.urlencode({
            'client': 't',
            'text': text.encode('utf-8'),
            'sl': source_lang,
            'tl': dest_lang,
            'ie': 'UTF-8',
            'oe': 'UTF-8'
        })
        conn = httplib.HTTPSConnection('translate.google.com')
        conn.request('GET', '/translate_a/t?' + params, headers={ 'User-Agent': 'Mozilla/5.0' })
        httpresponse = conn.getresponse().read().replace(",,,", ",\"\",\"\",").replace(",,", ",\"\",")
        response = json.loads("{\"response\":" + httpresponse + "}")
        return response['response'][0][0][0]
    except:
        return gettext('Error: Unexpected error.')
