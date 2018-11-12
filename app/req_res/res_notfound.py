# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/3
# 查找资源失败响应
from app.req_res.res_base import APIException


class NotFound(APIException):
    code = 0
    msg = 'the resource are not found O__O...'


class UserNotFound(NotFound):
    msg = 'the user are not exist'


class ItemNotFound(NotFound):
    msg = 'the item are not exist'


