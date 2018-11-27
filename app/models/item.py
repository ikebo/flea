"""
  Created by kebo on 2018/10/15
  Edit by wyb on 2018/10/30
"""
import datetime
from . import db
from app.models.base import Base
from app.utils import dict_get
from app.utils.enums import ItemTypeEnum
from sqlalchemy import orm


class Item(Base):
    __tablename__ = 'item'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    isSale = db.Column(db.SmallInteger, default=1)  # 物品销售状态(1表示在售 0表示下架 or 已卖出)

    # 物品必需信息
    itemName = db.Column(db.String(30))             # 物品标题/名称
    des = db.Column(db.String(250))                 # 物品描述
    type = db.Column(db.SmallInteger, default=ItemTypeEnum.OTHER_PRODUCTS.value)    # 物品分类(默认为其他)
    time = db.Column(db.DateTime)                   # 发布时间
    srcs = db.Column(db.String(300))                # 物品图片地址 (最多九张，分割符为'|')
    originPrice = db.Column(db.Integer)             # 物品原价
    price = db.Column(db.Integer)                   # 物品价格

    # 相关统计
    viewNum = db.Column(db.Integer)                 # 查看数
    goodNum = db.Column(db.Integer)                 # 点赞数
    collectNum = db.Column(db.Integer)              # 收藏数
    commentNum = db.Column(db.Integer)              # 评论数

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))               # 物品用户id
    comments = db.relationship('Comment', backref='item', lazy='dynamic')   # 物品的所有评论

    @orm.reconstructor  # ORM通过元类来创建模型对象 所以要在构造函数前添加这个装饰器 用以实现对象转字典
    def __init__(self):
        super(Item, self).__init__()
        # self.fields定义默认输出字段
        self.fields = ["id", "isSale", "type", "itemName", "time", "srcs", "des", "price", "user_id"]

    def edit_item(self, kwargs):
        """
        编辑物品信息
        :param kwargs: 物品类别  物品姓名 物品描述 物品图片地址 物品价格
        :return:
        """
        try:
            type = dict_get(kwargs, 'itemType')
            itemName = dict_get(kwargs, 'itemName')
            des = dict_get(kwargs, 'des')
            srcs = dict_get(kwargs, 'srcs')
            price = dict_get(kwargs, 'price')
            if type is not None:
                self.type = type
            if itemName is not None:
                self.itemName = itemName
            if des is not None:
                self.des = des
            if srcs is not None:
                self.srcs = srcs
            if price is not None:
                self.price = price
            self.save()
            return True
        except Exception as e:
            print(e)
        return False

    @staticmethod
    def create_item(kwargs, user_id):
        """
        创建物品
        :param kwargs:   物品类别  物品姓名 物品描述 物品图片地址 物品原价 物品价格
        :param user_id:  用户id
        :return:
        """
        try:
            print(kwargs)
            item = Item()
            item.type = dict_get(kwargs, 'type', ItemTypeEnum.OTHER_PRODUCTS.value)
            item.itemName = dict_get(kwargs, 'itemName', '')
            item.des = item.itemName + "\n" + dict_get(kwargs, 'des', '')  # 描述中最前面是物品名称
            item.time = datetime.datetime.now()
            item.srcs = dict_get(kwargs, 'srcs', '')
            item.originPrice = dict_get(kwargs, 'originPrice', -1)
            item.price = dict_get(kwargs, 'price', -1)
            item.user_id = user_id
            item.save()
            return True
        except Exception as e:
            print(e)
        return False

    @staticmethod
    def search_item(search_key, page_num):
        """
        根据传入的参数查询item
        :param search_key: 搜索关键字
        :param page_num: 指定返回范围
        :return:
        """
        from app.models.user import User            # 防止相互导入
        query = Item.query.join(User)
        items = query.filter(Item.des.like(search_key)).order_by(Item.time.desc()).offset(page_num * 8).limit(8).all()
        data = [dict(i) for i in items]
        return data

    def raw(self):
        if not self.time:
            self.time = datetime.datetime.now()
        return dict(id=self.id, type=self.type, des=self.des, srcs=self.srcs, user_id=self.user_id,
                    time=self.time.strftime('%Y-%m-%d-%H-%M-%S'), user=self.user.seri())

    def __repr__(self):
        return '<Item %s>' % self.itemName
