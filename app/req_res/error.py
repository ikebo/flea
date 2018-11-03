# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/3
# 自定义异常响应
from app.req_res.base import APIException


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999


class SomethingError(APIException):
    code = 500
    msg = 'something error'
    error_code = 999


class ClientTypeError(APIException):
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class PasswordError(APIException):
    code = 400
    msg = 'password is wrong'
    error_code = 1001


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class FileNameException(APIException):
    code = 400
    msg = 'the name of file is wrong!'
    error_code = 1001


class ChoiceImgException(APIException):
    code = 400
    msg = 'please choose a img!'
    error_code = 1002


class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = 'authorization failed'


class ImgLargeException(APIException):
    code = 403
    msg = 'the img is too large!'
    error_code = 1006


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'


