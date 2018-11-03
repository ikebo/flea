# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/31
# 转换相关代码
import json
from flask import request
from app.req_res import FileNameException, ChoiceImgException


class Transfer(object):
    """
        Transfer类: 处理请求参数
    """
    def __init__(self):
        self.postForm = request.form            # 取得post提交的表单
        self.getArgs = request.args             # 取得get提交的参数
        self.postValues = request.values        # 取得post提交的参数
        self.postData = request.data            # 取得post提交的数据
        self.fileData = request.files

    def handle_get(self):
        # 将get提交的参数转换成字典返回
        return self.getArgs.to_dict()

    def handle_post(self):
        # 将post数据转换成字典返回
        return json.loads(str(self.postData, encoding='utf-8').replace("'", "\""))

    def handle_file(self):
        # 处理提交的文件数据
        data = self.fileData
        if 'img' not in data:
            raise FileNameException
        file = data['img']
        if file.filename == '':
            raise ChoiceImgException
        return file
