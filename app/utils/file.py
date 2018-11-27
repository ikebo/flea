# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/1
# 文件相关操作
import os
import uuid
import datetime
from flask import current_app, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from app.req_res import ImgLargeException, SomethingError


def _get_current_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")


def _get_fileRoute(filename):
    """
    获取上传文件保存路径
    :param filename: 文件名
    :return:
    """
    file = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1].lower()
    folder = os.path.join(current_app.config['UPLOAD_FOLDER'], _get_current_date())
    if not os.path.exists(folder):
        os.mkdir(folder)
    return os.path.join(folder, file)


def allowed_file(filename):
    """
    检查文件是否合法
    :param filename:
    :return:
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_upload_img(file, filename):
    """
    保存上传的图片
    :param file:
    :param filename:
    :return: 返回图片存储地址
    """
    try:
        filename = secure_filename(filename)        # 对文件名进行检查
        path = _get_fileRoute(filename)
        print("the file save path: ", path)
        file.save(path)
        sep = os.path.sep
        ra = path.rsplit(sep, 3)            # uploads %Y-%m-%d xxx.xxx
        r = url_for('static', filename=(ra[-3] + '/' + ra[-2] + '/' + ra[-1]))      # 图片存储的链接地址
        print(r)
        data = dict(imgServerPath=r)
        return data
    except Exception as e:
        print(e)
        raise ImgLargeException() if isinstance(e, RequestEntityTooLarge) else SomethingError()

