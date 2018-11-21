from . import db
from app.models.base import Base
from app.req_res import *
from app.utils import dict_get
from flask_sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash                # 加密密码以及检测hash过的密码
import json


class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    isAuth = db.Column(db.SmallInteger, default=0)              # 是否完成认证 0表示未认证 1表示已认证

    # 微信信息
    openId = db.Column(db.String(100))                          # 微信openid
    nickName = db.Column(db.String(30))                         # 微信用户名
    avatarUrl = db.Column(db.String(100))                       # 微信头像地址

    # 联系方式
    phoneNumber = db.Column(db.String(11))                      # 手机号
    qqNumber = db.Column(db.String(11))                         # qq 号
    weixinNumber = db.Column(db.String(20))                     # 微信号

    # 个人真实信息
    realName = db.Column(db.String(20))                         # 姓名
    sex = db.Column(db.SmallInteger)                            # 性别
    stuId = db.Column(db.String(20))                            # 学号
    stuPwd = db.Column(db.String(100))                          # 教务系统密码

    clsName = db.Column(db.String(20))                          # 班级
    department = db.Column(db.String(20))                       # 院系

    # 所有物品，评论，回复
    items = db.relationship('Item', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    replies = db.relationship('Reply', backref='user', lazy='dynamic')

    @orm.reconstructor  # ORM通过元类来创建模型对象 所以要在构造函数前添加这个装饰器 用以实现对象转字典
    def __init__(self):
        super(User, self).__init__()
        self.fields = ["id", "isAuth", "openId", "nickName", "avatarUrl", "phoneNumber", "qqNumber", "weixinNumber"]

    @property
    def password(self):
        return self.stuPwd

    @password.setter
    def password(self, raw):
        self.stuPwd = generate_password_hash(raw)

    def check_password(self, raw):
        if not self.stuPwd:
            return False
        return check_password_hash(self.stuPwd, raw)

    @staticmethod
    def query_user_by_openId(openId):
        """
        通过openId查询用户
        :param openId: 微信openId
        :return:
        """
        user = User.query.filter_by(openId=openId).first()
        return user

    @staticmethod
    def query_user_by_id(user_id):
        """
        通过用户id查询用户
        :param user_id: 用户id
        :return:
        """
        user = User.query.filter_by(id=user_id).first()
        return user

    @staticmethod
    def query_items_by_id(user_id):
        """
        根据用户id获取用户发布的物品信息
        若用户没有物品返回ItemNotFound
        :return:
        """
        # todo: 后期看可不可以不借助Item类
        try:
            from app.models.item import Item                    # 防止相互导入
            items = Item.query.filter_by(user_id=user_id)
            return items
        except Exception as e:
            print(e)
            raise ItemNotFound() if isinstance(e, NotFound) else SomethingError()

    def is_auth(self):
        """
        判断是否已经认证
        :return:
        """
        if self.isAuth == 1:
            return True
        else:
            return False

    def set_auth(self):
        """
        设置authentication
        :return:
        """
        try:
            self.isAuth = 1
            self.save()
        except Exception as e:
            print(e)

    def update_avatar(self, kwargs):
        """
        更新头像和姓名
        :param kwargs:
        :return:
        """
        try:
            avatarUrl = dict_get(kwargs, 'avatarUrl')
            nickName = dict_get(kwargs, 'nickName')
            if avatarUrl is not None:
                self.avatarUrl = avatarUrl
            if nickName is not None:
                self.nickName = nickName
            if avatarUrl is None and nickName is None:                  # 两者不能都为空
                return False
            self.save()
            return True
        except Exception as e:
            print('Exception ', e)
            return False

    def update_contact(self, kwargs):
        """
        更新联系方式(电话号码、QQ号、微信号)
        :param kwargs:
        :return:
        """
        try:
            phoneNumber = dict_get(kwargs, 'phoneNumber')
            qqNumber = dict_get(kwargs, 'qqNumber')
            weixinNumber = dict_get(kwargs, 'weixinNumber')
            if phoneNumber is not None:
                self.phoneNumber = phoneNumber
            if qqNumber is not None:
                self.qqNumber = qqNumber
            if weixinNumber is not None:
                self.weixinNumber = weixinNumber
            if not phoneNumber and not qqNumber and not weixinNumber:       # 三种联系方式不能都为None
                return False
            self.save()
            return True
        except Exception as e:
            print('Exception ', e)
            return False

    def seri(self):
        return dict(id=self.id, avatarUrl=self.avatarUrl,
                    nickName=self.nickName, phoneNumber=self.phoneNumber)

    def raw(self):
        return dict(id=self.id, avatarUrl=self.avatarUrl,
                    nickName=self.nickName, phoneNumber=self.phoneNumber,
                    qqNumber=self.qqNumber, weixinNumber=self.weixinNumber)

    def get_contact(self):
        phoneNumber = self.phoneNumber
        qqNumber = self.qqNumber
        weixinNumber = self.weixinNumber

        return json.dumps(dict(phoneNumber=phoneNumber, qqNumber=qqNumber, weixinNumber=weixinNumber))

    @staticmethod
    def register_by_openid(openid):
        try:
            user = User()
            user.openId = openid
            user.save()
            return user, None
        except Exception as e:
            return None, e

    @staticmethod
    def is_exists_by_openid(openid):
        user = User.query.filter_by(openId=openid).first()
        if user is not None:
            return user, None
        else:
            return None, 'no this user'

    def __repr__(self):
        return "<User %r>" % self.nickName

