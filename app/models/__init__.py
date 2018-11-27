from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from app.req_res import *
from sqlalchemy.orm import loading
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    """
        重写SQLAlchemy
            auto_commit: 增加自动commit和出错自动回滚机制
            使用实例:
                with db.auto_commit():
                    user = User.query.filter_by(id=uid).first_or_404()
                    user.delete()
    """
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    """
    在这重写flask_sqlalchemy封装的查询 BaseQuery是继承了orm.query
        all方法:
            没有就raise一个NotFound异常
        get方法:
            实现根据id返回元素 存在就返回该元素 不存在就raise一个NotFound异常
        get_or_404方法:
            实现根据id返回元素 存在就返回该元素 不存在就raise一个NotFound异常
        first_or_404方法:
            实现返回Query元素的第一个值，为None就raise一个NotFound异常
        filter_by方法:
            实现pythonic的查找系列元素  存在就返回该系列元素 不存在就raise一个NotFound异常
    """
    # 有就返回 没有就raise一个NotFound异常
    def all(self):
        # print(len(list(self)))        # 当self为空时 len(list(self))为0
        if len(list(self)) is 0:
            raise NotFound()
        return list(self)

    # 有就返回 没有就raise一个NotFound异常
    def get(self, ident):
        rv = self._get_impl(ident, loading.load_on_pk_identity)
        if not rv:
            raise NotFound()
        return rv

    # 有就返回 没有就raise一个NotFound异常
    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    # 有就返回 没有就raise一个NotFound异常
    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv

    def filter_by(self, **kwargs):
        """
        目前是调用父类的filter_by执行 日后改成在未删除的元素中寻找
        :param kwargs:
        :return:
        """
        # if 'status' not in kwargs.keys():
        #     kwargs['status'] = 1  # 确保status为0的不被找出来
        res = super(Query, self).filter_by(**kwargs)
        if res.first() is None:
            raise NotFound()
        return res


# 实例化db
db = SQLAlchemy(query_class=Query)


# 只有导入Model才会在数据库建表
from . import user
from . import item
from . import comment
from . import reply
