"""
  Created by kebo on 2018/11/7
"""
from . import app
import requests


def is_code_valid(code):
    session_api = app.config['SESSION_API']
    target_api = session_api.format(app.config['APP_ID'], app.config['APP_SECRET'], code)
    r = requests.get(target_api).json()
    if 'errcode' in r:
        return '', r['errmsg']
    return r['openid'], None
