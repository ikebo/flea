# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/31
"""
app/api/v1/advice.py
==========================
advice的API:
    /api/v1/advice              POST            提交建议
    /api/v1/advice              GET             获取昨天的建议
    /api/v1/advice/advices      GET             获取所有建议

"""
from . import Redprint
from app.req_res import *
from app.req_res.req_transfer import Transfer
from app.utils.advice import Advice

api = Redprint("advice")


@api.route('/', methods=['POST'])
def post_advice():
    """
    提交建议
    :return:
    """
    try:
        transfer = Transfer()
        advice = Advice()
        data = transfer.handle_post()
        user_id, advice_content = data['user_id'], data['advice']
        advice.save_advice(user_id, advice_content)
        return dict(code=1, msg='post advice successfully')
    except Exception as e:
        print(e)
    return SomethingError()


@api.route('/', methods=["GET"])
def get_advice():
    """
    获取昨天的建议
    :return:
    """
    try:
        advice = Advice()
        data = advice.get_yesterday_advice()
        return dict(code=1, msg='get yesterday advices successfully', data=data)
    except Exception as e:
        print(e)
    return SomethingError()


@api.route('/advices', methods=["GET"])
def get_advices():
    """
    获取所有建议
    :return:
    """
    try:
        advice = Advice()
        data = advice.get_all_advice()
        return dict(code=1, msg='get all advices successfully', data=data)
    except Exception as e:
        print(e)
    return SomethingError()

