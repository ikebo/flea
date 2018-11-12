# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/1
# 测试一些东西用的路由
from . import Redprint
from app.req_res.req_transfer import Transfer

test = Redprint("test")


# 测试封装的获取数据和返回数据
@test.route('/', methods=['GET'])
def just_test():
    transfer = Transfer()
    # 获取get参数
    dic = transfer.handle_get()
    print(dic)
    return dict(msg='成功获取get参数', data=dic)


# 测试封装的获取数据和返回数据
@test.route('/', methods=['POST'])
def just_test2():
    transfer = Transfer()
    # 获取post参数
    dic = transfer.handle_post()
    print(dic)
    return dict(msg='成功获取post参数', data=dic)