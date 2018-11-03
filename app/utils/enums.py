# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
"""
app/utils/enums.py
======================
枚举:
    登陆类型的枚举 -> ClientTypeEnum
    物品类型的枚举 -> ItemTypeEnum

"""
from enum import Enum


class ClientTypeEnum(Enum):
    USER_EMAIL = 100
    USER_MOBILE = 101

    # 微信小程序
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201


class ItemTypeEnum(Enum):
    # 运动用品 学习用品 电子产品
    SPORT_PRODUCTS = 1
    STUDY_PRODUCTS = 2
    ELECTRON_PRODUCTS = 3

    # 生活用品 其他用品
    LIFE_PRODUCTS = 6
    OTHER_PRODUCTS = 8


