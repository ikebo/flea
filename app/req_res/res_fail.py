# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/12
# 异常响应
from app.req_res.res_base import APIException


class Fail(APIException):
    code = 2
    msg = 'Fail'


class UpdateFail(Fail):
    # 更新失败
    msg = 'fail to update'


class AuthFail(Fail):
    # 认证失败
    msg = 'fail to auth(id is wrong or password is wrong)'




