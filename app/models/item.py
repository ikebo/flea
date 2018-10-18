"""
  Created by kebo on 2018/10/15
"""
import datetime

from . import db

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    type = db.Column(db.SmallInteger)  # 物品分类
    itemName = db.Column(db.String(30))  # 物品标题/名称
    time = db.Column(db.DateTime)      # 发布时间
    srcs = db.Column(db.String(300))   # 物品图片地址 (最多三张，分割符为'|')
    des = db.Column(db.String(250))    # 物品描述
    viewNum = db.Column(db.Integer)    # 查看数
    goodNum = db.Column(db.Integer)    # 点赞数
    commentNum = db.Column(db.Integer) # 评论数
    price = db.Column(db.Integer)      # 物品价格
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 物品用户id
    comments = db.relationship('Comment', backref='item', lazy='dynamic') # 物品的所有评论

    def __init__(self, type, itemName, srcs, des, price, user_id):
        self.type = type
        self.itemName = itemName
        self.time = datetime.datetime.now()
        self.srcs = srcs
        self.des = des
        self.price = price
        self.user_id = user_id

    def __repr__(self):
        return '<Item %s>' % self.itemName