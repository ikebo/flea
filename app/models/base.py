# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/10
from datetime import datetime
from app.models import db


# 数据类基类
class Base(db.Model):
    """
        重写db.Model
            重写一些方法 添加一些新属性新方法
    """
    __abstract__ = True

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
        # 获得创建时间
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    # 设置对象的属性(id不能设置)
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        """
        删除记录 ->目前是真删除 日后可能改成假删除 -> self.status = 0
        :return:
        """
        with db.auto_commit():
            db.session.delete(self)

    def save(self):
        """
        保存修改或提交的记录
        :return:
        """
        with db.auto_commit():
            db.session.add(self)

    @classmethod
    def all(cls):
        """
        封装返回所有对象
        实际上就是执行这样的代码: items = Item.query.all()
        :return:
        """
        return cls.query.all()

    def keys(self):
        # 返回fields属性 -> fields属性定义默认输出字段
        return self.fields

    def hide(self, *keys):
        # 减少fields属性中的值
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        # 增加fields属性中的值
        for key in keys:
            self.fields.append(key)
        return self


