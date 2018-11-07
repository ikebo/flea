from . import db

class User(db.Model):
    __tablename__  = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # 微信信息
    openId = db.Column(db.String(100))  # 微信openid
    nickName = db.Column(db.String(30))  # 微信用户名
    avatarUrl = db.Column(db.String(100)) # 微信头像地址

    # 联系方式
    phoneNumber = db.Column(db.String(11)) # 手机号
    qqNumber = db.Column(db.String(11))    # qq 号
    weixinNumber = db.Column(db.String(20)) # 微信号

    # 个人真实信息
    realName = db.Column(db.String(20))  # 姓名
    sex = db.Column(db.SmallInteger)     # 性别
    stuId = db.Column(db.String(20))     # 学号
    stuPwd = db.Column(db.String(100))   # 教务系统密码(加密)
    isAuth = db.Column(db.SmallInteger)  # 是否完成认证
    clsName = db.Column(db.String(20))   # 班级
    department = db.Column(db.String(20)) # 院系

    # 所有物品，评论，回复
    items = db.relationship('Item', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    replies = db.relationship('Reply', backref='user', lazy='dynamic')


    def __init__(self, openId):
        self.openId = openId

    def json(self):
        return dict(id=self.id, nickName=self.nickName, avatarUrl=self.avatarUrl)

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