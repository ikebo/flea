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
from app.models.user import User
from app.req_res import *
from app.req_res.res import Res
from app.req_res.transfer import Transfer
from app.utils.http import request_auth
from app.utils.util import is_code_valid

user = Redprint("user")

# 所有返回值最终为以下格式
# {
#    code: (0 or 1 or 2) <1表示成功， 0表示正常失败，2表示有异常>
#    msg: <提示信息>
#    data: <需要返回的数据，格式为dict, 没有可不填>
# }
# 但是每次这样返回很繁琐，所在在app.__init__.py 中重写了app.response_class
# 可直接返回dict, tuple or list, 若为dict, 则格式为 dict(code=.., msg=.., data)
# 若为tuple, 因为flask中直接返回 a, b, c格式的话会自动调用make_response， 所以格式为
# (code, msg, data<没有可不填，默认为None>), status_code, headers
# 若为list, 格式为 [code, msg, data<没有可不填，默认为None>]


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
            return UserNotFound()
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
        return UserNotFound()
    else:
        return Res(1, 'get user successfully', u.raw()).jsonify()


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
        return UserNotFound()

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
        return UserNotFound()

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
            if u is None:
                return UserNotFound()
            if u.set_auth():
                return AuthSuccess()
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
        return UserNotFound()
    if u.delete():
        return DeleteSuccess()
    else:
        return SomethingError()


# 测试用
@user.route('')
def get_user():
    return (1, 'success', dict(a='code')), 203


# 用户登录, 前端根据获取的code调用此接口
# 首先判断code是否有效，无效则返回非法code, 有效则可以获取用户的openid
# 然后根据openid查询用户，如无此用户则创建，最终返回用户信息
@user.route('/<code>', methods=['GET'])
def login(code):
    # 根据code获取openid, 若code无效，则nil不为空
    openid, nil = is_code_valid(code)
    if nil is not None:
        return (0, 'invalid code'), 400
    else:
        user, nil = User.is_exists_by_openid(openid)
        if nil is not None:
            # 注册此用户
            user, nil = User.register_by_openid(openid)
            if nil is not None:
                return (2, 'fail to register user'), 500
            else:
                return (1, 'register user successfully', user.json()), 200
        else:
            return (1, 'old user', user.json()), 200


