"""
  Created by kebo on 2018/10/15
"""
import datetime
from . import db
from app.models.base import Base
from flask_sqlalchemy import orm


class Comment(Base):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    content = db.Column(db.String(100))                                     # 评论内容
    time = db.Column(db.DateTime)                                           # 评论时间
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))               # 评论所属物品id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))               # 评论所属用户id

    replies = db.relationship('Reply', backref='comment', lazy='dynamic')   # 评论下的所有回复

    @orm.reconstructor  # ORM通过元类来创建模型对象 所以要在构造函数前添加这个装饰器 用以实现对象转字典
    def __init__(self, content, item_id, user_id):
        super(Comment, self).__init__()
        self.content = content
        self.time = datetime.datetime.now()
        self.item_id = item_id
        self.user_id = user_id

    def __repr__(self):
        return '<Comment %s>' % self.content
