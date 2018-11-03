# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/3
# 自定义成功响应
from app.req_res.base import APIException


class Success(APIException):
    code = 201
    msg = 'Ok - success'
    error_code = 0


class EditSuccess(Success):
    msg = 'edit success'


class PostSuccess(Success):
    msg = 'post success'


class UpdateSuccess(Success):
    msg = 'update success'


class DeleteSuccess(Success):
    code = 202                      # 204表示No Content 在返回中没有任何内容
    msg = 'delete success'



