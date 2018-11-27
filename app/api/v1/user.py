"""
    Created by kebo on 2018/10/16
    Edited by wyb on 2018/10/31

    app/api/v1/user.py:
    user相关API  
        /api/v1/user/                           GET   			获取所有用户信息
        /api/v1/user/<int:user_id>              GET             根据用户id获取用户信息
        /api/v1/user/<code>                     GET             获取用户openId
        /api/v1/user/publish/<int:user_id>      GET             获取用户发布的所有物品信息
        /api/v1/user/avatar/<int:user_id>       POST            更新头像和名字
        /api/v1/user/contact/<int:user_id>      POST            更新联系方式
        /api/v1/user/auth/<int:user_id>         GET             判断用户是否认证
        /api/v1/user/auth                       POST            用户认证
        /api/v1/user/<int:user_id>              DELETE          删除用户
"""
from . import Redprint
from app.models.user import User
# from app.req_res import *
# from app.req_res.req_transfer import Transfer
# from app.utils.http import request_auth
from app.utils.util import is_code_valid
from flask import g

user = Redprint("user")


# @user.route('/', methods=['GET'])
# def get_users():
#     """
#     获取所有用户信息
#     :return:
#     """
#     try:
#         users = User.query.all()
#         data = [dict(u) for u in users]
#         return dict(code=1, msg='get users successfully', data=data)
#     except Exception as e:
#         print(e)
#         return UserNotFound() if isinstance(e, NotFound) else SomethingError()
#
#
# @user.route('/detail/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     """
#     根据用户id获取用户信息
#     :param user_id:
#     :return:
#     """
#     try:
#         u = User.query_user_by_id(user_id)
#         return dict(code=1, msg='get user successfully', data=dict(u))
#     except Exception as e:
#         print(e)
#         return UserNotFound() if isinstance(e, NotFound) else SomethingError()
#
#
# @user.route('/publish/<int:user_id>', methods=['GET'])
# def publish_item(user_id):
#     """
#     获取某个用户发布的所有物品信息
#     :param user_id:
#     :return:
#     """
#     try:
#         u = User.query_user_by_id(user_id)
#         items = User.query_items_by_id(u.id)
#         data = [dict(i) for i in items]
#         return dict(code=1, msg='get user successfully', data=data)
#     except Exception as e:
#         print(e)
#         if isinstance(e, ItemNotFound):
#             return ItemNotFound()
#         elif isinstance(e, NotFound):
#             return UserNotFound()
#         return SomethingError()
#
#
# @user.route('/avatar/<int:user_id>', methods=['POST'])
# def update_avatar(user_id):
#     """
#     更新头像和姓名
#     :param user_id:
#     :return:
#     """
#     try:
#         transfer = Transfer()
#         u = User.query_user_by_id(user_id)
#         data = transfer.handle_post()
#         if u.update_avatar(data):
#             return UpdateSuccess()
#         else:
#             return UpdateFail()
#     except Exception as e:
#         print(e)
#         return UserNotFound() if isinstance(e, NotFound) else SomethingError()
#
#
# @user.route('/contact/<int:user_id>', methods=['POST'])
# def update_contact(user_id):
#     """
#     更新联系方式
#     :param user_id:
#     :return:
#     """
#     try:
#         transfer = Transfer()
#         u = User.query_user_by_id(user_id)
#         data = transfer.handle_post()
#         print(data)
#         if u.update_contact(data):
#             return UpdateSuccess()
#         else:
#             return UpdateFail()
#     except Exception as e:
#         print(e)
#         return UserNotFound() if isinstance(e, NotFound) else SomethingError()
#
#
# @user.route('/auth/<int:user_id>', methods=['GET'])
# def is_auth(user_id):
#     """
#     判断用户是否认证
#     :return:
#     """
#     try:
#         u = User.query_user_by_id(user_id)
#         if u.is_auth():
#             return dict(code=1, msg='user is auth')
#         else:
#             return dict(code=0, msg='user is not auth')
#     except Exception as e:
#         print(e)
#         return UserNotFound() if isinstance(e, NotFound) else SomethingError()
#
#
# @user.route('/auth', methods=['POST'])
# def auth():
#     """
#     认证
#     :return:
#     """
#     try:
#         transfer = Transfer()
#         data = transfer.handle_post()
#         print(data)
#         user_id, stu_id, stu_pwd = data['user_id'], data['stu_id'], data['stu_pwd']
#         if request_auth(stu_id, stu_pwd):
#             u = User.query.get(user_id)
#             u.set_auth()
#             return AuthSuccess()
#         else:
#             return AuthFail()
#     except Exception as e:
#         print(e)
#         return UserNotFound() if isinstance(e, NotFound) else SomethingError()
#
#
# @user.route('/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     """
#     删除用户
#     :param user_id:
#     :return:
#     """
#     try:
#         u = User.query.get(user_id)
#         u.delete()
#     except Exception as e:
#         print(e)
#         return UserNotFound() if isinstance(e, NotFound) else SomethingError()
#     else:
#         return DeleteSuccess()



# 用户登录, 前端根据获取的code调用此接口
# 首先判断code是否有效，无效则返回非法code, 有效则可以获取用户的openid
# 然后根据openid查询用户，如无此用户则创建，最终返回用户信息
@user.route('/login/<code>', methods=['GET'])
def login(code):
    # 根据code获取openid, 若code无效，则nil不为空
    openid, nil = is_code_valid(code)
    if nil is not None:
        return (0, 'invalid code'), 400
    else:
        user, nil = User.is_exists_by_openid(openid)
        if nil is not None:
            # 注册此用户 然后 并保存用户信息到g变量中
            user, nil = User.register_by_openid(openid)
            g.user = user
            if nil is not None:
                return (2, 'fail to register user'), 500
            else:
                return (1, 'register user successfully', user.seri()), 200
        else:
            g.user = user  # 保存用户信息到g变量中
            return (1, 'old user', user.seri()), 200


