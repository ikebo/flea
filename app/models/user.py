from . import db
from app.utils import dict_get
from werkzeug.security import generate_password_hash, check_password_hash                # 加密密码以及检测hash过的密码
import json


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # 相关状态
    status = db.Column(db.SmallInteger, default=1)              # 数据状态(日后实现假删除) 1表示存在 0表示删除
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

    def __init__(self, openId):
        self.openId = openId

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

    def set_auth(self):
        """
        设置authentication
        :return:
        """
        try:
            self.isAuth = 1
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False

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
            db.session.add(self)
            db.session.commit()
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
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print('Exception ', e)

        return False

    def delete(self):
        """
        删除对象 - 直接删除
        :return:
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False


    def seri(self):
        return dict(id=self.id, avatarUrl=self.avatarUrl,
                    nickName=self.nickName, phoneNumber=self.phoneNumber)

    def raw(self):
        return dict(id=self.id, avatarUrl=self.avatarUrl,
                    nickName=self.nickName, phoneNumber=self.phoneNumber,
                    qqNumber=self.qqNumber, weixinNumber=self.weixinNumber)


    @staticmethod
    def register_by_openid(openid):
        try:
            user = User(openid)
            db.session.add(user)
            db.session.commit()
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

