# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/3
# 自定义正常失败的响应
from app.req_res.res_base import APIException


class Error(APIException):
    # 正常失败的基类
    code = 0


class ServerError(APIException):
    # 表示一个未知异常
    code = 2
    msg = 'sorry, we made a mistake (*￣︶￣)!'


class SomethingError(Error):
    # 表示一个未知异常
    code = 2
    msg = 'something error'


class ClientTypeError(Error):
    msg = 'client is invalid'


class PasswordError(Error):
    msg = 'password is wrong'


class ParameterException(Error):
    msg = 'invalid parameter'


class FileNameException(Error):
    msg = 'the name of file is wrong!'


class ChoiceImgException(Error):
    msg = 'please choose a img!'


class ImgLargeException(Error):
    msg = 'the img is too large!'


class Forbidden(Error):
    msg = 'forbidden, not in scope'


class UserNoItems(Error):
    msg = 'user no items'

