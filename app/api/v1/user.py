"""
  Created by kebo on 2018/10/16
"""
from app.models.user import User
from . import Redprint
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

