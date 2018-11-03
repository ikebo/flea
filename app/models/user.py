from . import db
import json


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # 微信信息
    openId = db.Column(db.String(100))                  # 微信openid
    nickName = db.Column(db.String(30))                 # 微信用户名
    avatarUrl = db.Column(db.String(100))               # 微信头像地址

    # 联系方式
    phoneNumber = db.Column(db.String(11))              # 手机号
    qqNumber = db.Column(db.String(11))                 # qq 号
    weixinNumber = db.Column(db.String(20))             # 微信号

    # 个人真实信息
    realName = db.Column(db.String(20))                 # 姓名
    sex = db.Column(db.SmallInteger)                    # 性别
    stuId = db.Column(db.String(20))                    # 学号
    clsName = db.Column(db.String(20))                  # 班级
    department = db.Column(db.String(20))               # 院系

    # 所有物品，评论，回复
    items = db.relationship('Item', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    replies = db.relationship('Reply', backref='user', lazy='dynamic')

    def __init__(self, openId):
        self.openId = openId

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
        try:
            self.qqNumber = '1'
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
            self.avatarUrl = kwargs['avatarUrl']
            self.nickName = kwargs['nickName']
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
            self.phoneNumber = kwargs.get('phoneNumber', None)
            self.qqNumber = kwargs.get('qqNumber', None)
            self.weixinNumber = kwargs('weixinNumber', None)
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print('Exception ', e)

        return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def json(self):
        user_id = self.id
        openId = self.openId

        return json.dumps(dict(id=user_id, openId=openId))

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

    def __repr__(self):
        return "<User %r>" % self.nickName

