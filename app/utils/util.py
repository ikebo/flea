"""
  Created by kebo on 2018/11/7
"""
from flask import current_app
import requests


def is_code_valid(code):
    session_api = current_app.config['SESSION_API']
    target_api = session_api.format(current_app.config['APP_ID'], current_app.config['APP_SECRET'], code)
    r = requests.get(target_api).json()
    if 'errcode' in r:
        return '', r['errmsg']
    return r['openid'], None
