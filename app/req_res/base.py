# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/3
# req_res包的基类
from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    # 默认错误:
    code = 500
    msg = 'sorry, something error (*￣︶￣)!'
    error_code = 999            # 未知错误

    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)           # msg表示description None赋给response

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        # 取得url中的main_path
        # eg: localhost:3000/api/v1/user?user_id=1的main_path是localhost:3000/api/v1/user
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
