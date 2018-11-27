"""
    Created by kebo on 2018/10/16
    Edited by wyb on 2018/11/3
"""
# 基础工具函数


# 将bytes转换成str
def bytes_to_str(data):
    """

    :param data: 字符串 or bytes
    :return:
    """
    if isinstance(data, bytes):  # 如果是bytes转成str -> json无法dumps bytes
        data = str(data, encoding='utf-8')
    return data


# 读取文件内容
def read_file(path, mode):
    """

    :param path: 文件路径
    :param mode: 打开模式
    :return:
    """
    with open(path, mode) as f:
        content = f.read()
    return content


# dict的get实现
def dict_get(dic, key, default=None):
    """
    判断某个字典中是否有某个键 有就返回其对应的值 没有返回None
    :param dic: 字典
    :param key: 键
    :param default: 键不存在时返回的值
    :return:
    """
    if type(dic) is not dict:
        return None
    if key in dic:
        return dic[key]
    else:
        return default
