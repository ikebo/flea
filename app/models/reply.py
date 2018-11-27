"""
  Created by kebo on 2018/10/15
"""
import datetime
from . import db
from app.models.base import Base
from flask_sqlalchemy import orm


class Reply(Base):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    content = db.Column(db.String(100))                                             # 回复内容
    time = db.Column(db.DateTime)                                                   # 回复时间
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))                 # 回复所属评论id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))                       # 回复所属用户id

    @orm.reconstructor  # ORM通过元类来创建模型对象 所以要在构造函数前添加这个装饰器 用以实现对象转字典
    def __init__(self, content, comment_id, user_id):
        super(Reply, self).__init__()
        self.content = content
        self.time = datetime.datetime.now()
        self.comment_id = comment_id
        self.user_id = user_id

    def __repr__(self):
        return '<Reply %s>' % self.content


