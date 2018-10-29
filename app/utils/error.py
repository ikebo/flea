from flask import request, json
from werkzeug.exceptions import HTTPException
"""
app/utils/error.py
======================

自定义异常
    定义自定义异常基类APIException与一系列自定义异常类
    
下面是自定义的一系列异常:
 400 -> 请求参数错误  401 -> 未授权  403 -> 禁止访问  404 -> 没有找到资源或页面
 500 -> 服务器产生位置错误
 200 -> 查询成功  201 -> 创建或更新成功  204 -> 删除成功
"""


class APIException(HTTPException):
    # 默认错误:
    code = 500
    msg = 'sorry, something error (*￣︶￣)!'
    error_code = 999            # 未知错误

    def __init__(self, msg=None, code=None, error_code=None,
                 headers=None):
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


# 自定义异常类:
class Success(APIException):
    code = 201
    msg = 'Ok - success'
    error_code = 0


class DeleteSuccess(Success):
    code = 202                      # 204表示No Content 在返回中没有任何内容
    msg = 'delete success'
    error_code = -1


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999


class ClientTypeError(APIException):
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'the resource are not found O__O...'
    error_code = 1001


class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = 'authorization failed'


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'


class DuplicateGift(APIException):
    code = 400
    error_code = 2001
    msg = 'the current book has already in gift'


