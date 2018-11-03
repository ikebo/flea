"""
    Created by kebo on 2018/10/16
    Edited by wyb on 2018/11/3
"""
# 基础工具函数


# 将bytes转换成str
def bytes_to_str(data):
    if isinstance(data, bytes):  # 如果是bytes转成str -> json无法dumps bytes
        data = str(data, encoding='utf-8')
    return data


# 读取文件内容
def read_file(path, mode):
    with open(path, mode) as f:
        content = f.read()
    return content

