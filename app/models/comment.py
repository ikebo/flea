"""
  Created by kebo on 2018/10/15
"""
import datetime

from . import db


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # 相关状态
    status = db.Column(db.SmallInteger, default=1)                          # 数据状态(日后实现假删除) 1表示存在 0表示删除
    content = db.Column(db.String(100))                                     # 评论内容
    time = db.Column(db.DateTime)                                           # 评论时间
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))               # 评论所属物品id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))               # 评论所属用户id

    replies = db.relationship('Reply', backref='comment', lazy='dynamic')   # 评论下的所有回复

    def __init__(self, content, item_id, user_id):
        self.content = content
        self.time = datetime.datetime.now()
        self.item_id = item_id
        self.user_id = user_id

    def __repr__(self):
        return '<Comment %s>' % self.content
