# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/3
# req_res包的基类
from flask import request, json
from werkzeug.exceptions import HTTPException


# APIException -》 自定义异常基类
class APIException(HTTPException):
    # code: (0 or 1 or 2) <1表示成功， 0表示正常失败，2表示有异常>  msg: <提示信息>
    code = 2
    msg = 'sorry, something error (*￣︶￣)!'

    def __init__(self, msg=None, code=None, headers=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)           # msg表示description None赋给response

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
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
