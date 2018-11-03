"""
    Created by kebo on 2018/10/16
    Edited by wyb on 2018/10/31

    app/api/v1/user.py:
    user相关API  
        /api/v1/user/                           GET   			获取所有用户信息
        /api/v1/user/<int:user_id>              GET             根据用户id获取用户信息
        /api/v1/user/<code>                     GET             获取用户openId
        /api/v1/user/avatar/<int:user_id>       POST            更新头像和名字
        /api/v1/user/contact/<int:user_id>      POST            更新联系方式
        /api/v1/user/auth                       POST            用户认证
        /api/v1/user/<int:user_id>              DELETE          删除用户
"""
from . import Redprint
from flask import current_app
from app.models import db
from app.models.user import User
from app.req_res import *
from app.req_res.res import Res
from app.req_res.transfer import Transfer
from app.utils.http import HTTP
from app.utils.http import request_auth

user = Redprint("user")


@user.route('/', methods=['GET'])
def get_users():
    """
    获取所有用户信息
    :return:
    """
    try:
        users = User.query.all()
        users = [u.raw() for u in users]
        if users is None:
            return NotFound()
        return Res(1, 'get users successfully', users).jsonify()
    except Exception as e:
        print(e)
    return SomethingError()


@user.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    根据用户id获取用户信息
    :param user_id:
    :return:
    """
    u = User.query.get(user_id)
    if u is None:
        return NotFound()
    else:
        return Res(1, 'get user successfully', u.raw()).jsonify()


@user.route('/<code>', methods=['GET'])
def get(code):
    """
    获取openId
    :param code: 登陆凭证
    :return:
    """
    # 获得session_key， 用户的openId
    sessionApi = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'
    targetApi = sessionApi.format(current_app.config['APP_ID'], current_app.config['APP_SECRET'], code)

    # 返回值
    code, msg, data = 1, 'user does not exist, but has been registered.', None

    res = HTTP.get(targetApi)  # dict
    print(res)
    # code出错
    if 'errcode' in res:
        code, msg = 2, res['errmsg']
        return Res(code, msg, data).jsonify()

    # 正常, 获得openId
    openId = res['openid']
    u = User.query_user_by_openId(openId)

    # 根据user构造返回值
    if u is not None:
        code, msg = 1, 'user exist'
    else:
        u = User(openId)
        db.session.add(u)
        db.session.commit()

    return Res(code, msg, u.raw()).jsonify()


@user.route('/avatar/<int:user_id>', methods=['POST'])
def update_avatar(user_id):
    """
    更新头像和姓名
    :param user_id:
    :return:
    """
    transfer = Transfer()
    u = User.query_user_by_id(user_id)
    if u is None:
        return NotFound()

    data = transfer.handle_post()
    print(data)
    if u.update_avatar(data):
        return Res(1, 'update avatar successfully').jsonify()
    else:
        return SomethingError()


@user.route('/contact/<int:user_id>', methods=['POST'])
def update_contact(user_id):
    """
    更新联系方式
    :param user_id:
    :return:
    """
    transfer = Transfer()
    u = User.query_user_by_id(user_id)
    if u is None:
        return NotFound()

    data = transfer.handle_post()
    print(data)
    if u.update_contact(data):
        return Res(1, 'update contact successfully').jsonify()
    else:
        return SomethingError()


@user.route('/auth', methods=['POST'])
def auth():
    """
    认证
    :return:
    """
    try:
        transfer = Transfer()
        data = transfer.handle_post()
        print(data)
        user_id, stu_id, stu_pwd = data['user_id'], data['stu_id'], data['stu_pwd']
        if request_auth(stu_id, stu_pwd):
            u = User.query.get(user_id)
            if u.set_auth():
                return Res(1, 'success').jsonify()
        else:
            return PasswordError()
    except Exception as e:
        print(e)
        return SomethingError()


@user.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    删除用户
    :param user_id:
    :return:
    """
    u = User.query.get(user_id)
    if u is None:
        return NotFound()
    if u.delete():
        return DeleteSuccess()
    else:
        return SomethingError()


