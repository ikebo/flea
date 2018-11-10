# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/10
from datetime import datetime
from app.models import db


# 数据类基类
class Base(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # 相关状态
    status = db.Column(db.SmallInteger, default=1)  # 数据状态(日后实现假删除) 1表示存在 0表示删除
    create_time = db.Column(db.Integer)             # 创建时间(自动生成)

    def __init__(self):
        # 初始化创建时间
        self.create_time = int(datetime.now().timestamp())

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @classmethod
    def all(cls):
        """
        封装返回所有对象
        实际上就是执行这样的代码: items = Item.query.all()
        :return:
        """
        pass

    def delete(self):
        """
        目前是真删除 日后可能改成假删除 -> self.status = 0
        :return:
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self

    @classmethod
    def page(cls):
        """
        封装分页返回数据
        实际上就是执行这样的代码: Item.query.order_by(Item.time.desc()).offset(page_num * 8).limit(8).all()
        :return:
        """
        pass

