# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/31
import requests
import re
from pyquery import PyQuery as pq


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text


# 模拟登录
def request_auth(username, password):
    url = 'http://uia.whxy.edu.cn/cas/login'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JSESSIONID=7315B7866D151FA81AA418936677F345; Path=/cas; HttpOnly',
        'Host': 'uia.whxy.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    data = dict(username=username, password=password, _eventId='submit')
    res = requests.get(url)
    headers['Cookie'] = res.headers['Set-Cookie']
    lt_pattern = re.compile(r'value="(_c.*?)"')
    lt = re.search(lt_pattern, res.text).group(1)
    data['lt'] = lt
    pr = requests.post(url, data=data, headers=headers)
    return '用户登录' not in pq(pr.text)('title').text()


