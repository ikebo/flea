# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/3
# 自定义成功响应
from app.req_res.base import APIException


class Success(APIException):
    code = 1
    msg = 'Ok - success'


class AuthSuccess(Success):
    # 认证成功
    msg = 'auth success'


class EditSuccess(Success):
    # 编辑成功
    msg = 'edit success'


class PostSuccess(Success):
    # 提交成功
    msg = 'post success'


class UpdateSuccess(Success):
    # 更新成功
    msg = 'update success'


class DeleteSuccess(Success):
    # 删除成功
    msg = 'delete success'



