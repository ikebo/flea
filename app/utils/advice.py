# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/21
import os
import datetime
from flask import current_app
from app.utils import bytes_to_str, read_file


class Advice(object):
    def __init__(self):
        self.FILE_READ_MODE = "rb"                                                                      # 建议文件的读取模式
        self.ADVICE_FILENAME_FORMAT = "%Y-%m-%d"                                                        # 建议文件名的格式
        self.ADVICE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"                                                   # 建议中时间的格式
        self.ADVICE_FOLDER_PATH = current_app.config['ADVICE_PATH']                                     # 建议存储文件夹的路径
        self.NOWDAY_ADVICE_FILENAME = datetime.datetime.now().strftime(self.ADVICE_FILENAME_FORMAT)     # 今天的格式化时间(今天的建议文件名)

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        self.YESTERDAY_ADVICE_FILENAME = yesterday.strftime(self.ADVICE_FILENAME_FORMAT)                # 昨天的格式化时间(昨天的建议文件名)

    # 将建议格式化
    def _format_advice(self, user_id, advice_content):
        time = datetime.datetime.now().strftime(self.ADVICE_TIME_FORMAT)
        res = str(user_id) + '  ' + time + '\n' + str(advice_content) + '\n\n'
        return res

    # 获得今天建议文件的存储路径
    def _advice_route(self):
        if not os.path.exists(self.ADVICE_FOLDER_PATH):
            os.mkdir(self.ADVICE_FOLDER_PATH)
        advice_route = self.ADVICE_FOLDER_PATH + os.path.sep + self.NOWDAY_ADVICE_FILENAME

        return advice_route

    # 获取昨天建议文件的存储路径
    def _advice_route2(self):
        if not os.path.exists(self.ADVICE_FOLDER_PATH):
            os.mkdir(self.ADVICE_FOLDER_PATH)
        advice_route = self.ADVICE_FOLDER_PATH + os.path.sep + self.YESTERDAY_ADVICE_FILENAME

        return advice_route

    # 获取文件中的内容(rb)
    def _read_file_content(self, path):
        return read_file(path, self.FILE_READ_MODE)

    # 存储建议内容
    def save_advice(self, user_id, advice_content):
        try:
            advice_route = self._advice_route()
            with open(advice_route, 'a') as f:
                fmt_advice = self._format_advice(user_id, advice_content)
                f.write(fmt_advice)
        except Exception as e:
            print(e)

    # 获得今天存储的advice内容
    def get_nowday_advice(self):
        advice_router = self._advice_route()
        advice_content = self._read_file_content(advice_router)
        return bytes_to_str(advice_content)

    # 获得昨天存储的advice内容
    def get_yesterday_advice(self):
        advice_router = self._advice_route2()
        advice_content = self._read_file_content(advice_router)
        return bytes_to_str(advice_content)

    # 获取所有建议
    def get_all_advice(self):
        path = self.ADVICE_FOLDER_PATH
        data = {}
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            print(file_path)
            if os.path.isfile(file_path):
                advice_content = self._read_file_content(file_path)
                file_path = os.path.join(path, file).replace('/', '\\')         # 将Linux的分界符换成Windows的分界符
                advice_name = file_path.rsplit("\\", 1)[1]
                data[advice_name] = bytes_to_str(advice_content)
        return data

