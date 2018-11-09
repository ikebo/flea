# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/3
# 自定义异常响应
from app.req_res.base import APIException


class ServerError(APIException):
    msg = 'sorry, we made a mistake (*￣︶￣)!'


class SomethingError(APIException):
    msg = 'something error'


class ClientTypeError(APIException):
    code = 0
    msg = 'client is invalid'


class PasswordError(APIException):
    code = 0
    msg = 'password is wrong'


class ParameterException(APIException):
    code = 0
    msg = 'invalid parameter'


class FileNameException(APIException):
    code = 0
    msg = 'the name of file is wrong!'


class ChoiceImgException(APIException):
    code = 0
    msg = 'please choose a img!'


class AuthFailed(APIException):
    code = 0
    msg = 'authorization failed'


class ImgLargeException(APIException):
    code = 0
    msg = 'the img is too large!'


class Forbidden(APIException):
    code = 0
    msg = 'forbidden, not in scope'


