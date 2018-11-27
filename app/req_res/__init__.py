# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/3
# 请求和响应相关处理基类

# 导入所有自定义异常(success error notfound)供外部直接导入: from app.req_res import *
from .res_base import *
from .res_error import *
from .res_notfound import *
from .res_success import *
from .res_fail import *


