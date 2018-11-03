"""
  Created by kebo on 2018/7/28
"""
from flask import jsonify


class Res(object):
    """
        Res类: 处理返回结果
    """
    def __init__(self, code=1, msg='', data=None):
        """

        :param code: 默认为1 表示成功
        :param msg:
        :param data:
        """
        self.code = code
        self.msg = msg
        self.data = data

    def jsonify(self):
        """
        返回json格式数据的响应
        :return:
        """
        d = dict(code=self.code, msg=self.msg, data=self.data)
        return jsonify(d)

    def raw(self):
        """
        返回python原生字典格式的数据
        :return:
        """
        return dict(code=self.code, msg=self.msg, data=self.data)
