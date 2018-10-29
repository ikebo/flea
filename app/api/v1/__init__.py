"""
  Created by kebo on 2018/10/16
"""

from flask import Blueprint
from app.utils.redprint import Redprint   # 导入供其他红图模块使用

from .user import user
from .item import item
from .comment import comment
from .reply import reply


def create_blueprint_api_v1():
    api = Blueprint("api", __name__)
    user.register(api)
    item.register(api)
    comment.register(api)
    reply.register(api)
    return api
