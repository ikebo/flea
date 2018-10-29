"""
    app/api/v1/item.py:
    物品相关接口      物品接口前缀: /api/v1/item
        /   GET   								返回所有物品信息 page=xxx 指定返回范围
        /<int:item_id>   GET   					返回物品信息
        /<int: user_id>  POST    				发布物品信息
        /<int:item_id>   PUT   					修改物品信息
        /<int: item_id>  DELETE   				删除物品信息

        /upload_img             POST   			上传图片  返回图片地址
        /search	                GET			    搜索物品

"""

from . import Redprint
from flask import request, jsonify
from app.utils.error import APIException, NotFound
from app.utils.res import Res
from app.models.item import Item
from app.models.user import User

item = Redprint("item")


@item.route('/', methods=['GET'])
def get_item():
    """
    返回所有物品信息
    :return:
    """
    try:
        # page = int(request.args.get('page', -1))
        items = Item.query.all()
        data = [i.raw() for i in items]
        return jsonify(data)
    except Exception as e:
        print(e)
    return APIException()
    # return '返回物品信息'


@item.route('/<int:item_id>', methods=['GET'])
def return_item(item_id):
    """
    根据物品id得到物品的信息
    :param item_id: 物品id
    :return:
    """
    try:
        i = Item.query.filter_by(id=item_id).first_or_404()
        data = i.raw()
        return jsonify(data)
    except Exception as e:
        print(e)
        return e
    # return '返回某个物品信息'


@item.route('/<int:user_id>', methods=['POST'])
def post_item(user_id):
    return '发布物品信息'


@item.route('/<int:item_id>', methods=['PUT'])
def edit_item(item_id):
    return '修改物品信息'


@item.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    return '删除物品信息'


@item.route('/search', methods=['GET'])
def search_item():
    try:
        page = int(request.args.get('page'))  # 默认是字符串
        search_key = request.args.get('key')
        key = '%{}%'.format(search_key)
        print('key', key)
        query = Item.query.join(User)
        items = query.filter(Item.des.like(key)).order_by(Item.time.desc()).offset(page * 8).limit(8).all()
        data = [item.raw() for item in items]
        return jsonify(Res(1, 'search items successfully', data).raw())
    except Exception as e:
        print(e)
    return jsonify(Res(0, 'something error').raw())
    # return '搜索物品信息'

