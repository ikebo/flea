"""
    app/api/v1/item.py:
    item相关API
        /api/v1/item/   GET   								返回所有物品信息
        /api/v1/item/page/<int:page_num>   GET              访问部分物品信息 page_num指定返回范围
        /api/v1/item/<int:item_id>   GET   					返回某个物品详细信息
        /api/v1/item/<int: user_id>  POST    				发布物品信息
        /api/v1/item/<int:item_id>   PUT   					修改某个物品信息
        /api/v1/item/<int: item_id>  DELETE   				删除某个物品信息

        /api/v1/item/search	                    POST			 搜索物品
        /api/v1/item/search	                    POST			 搜索物品
        /api/v1/item/upload_img                 POST   			上传图片  返回图片地址
"""
from . import Redprint
from app.req_res import *
from app.req_res.req_transfer import Transfer
from app.utils.file import allowed_file, save_upload_img
from app.models.item import Item
from app.models.user import User

item = Redprint("item")


@item.route('/', methods=['GET'])
def get_items():
    """
    返回所有物品基本信息及物品对应的发布者id
    :return:
    """
    try:
        data = Item.get_items()
        print(data)
        return dict(code=1, msg='get all item data successfully', data=data)
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '返回所有物品信息'


@item.route('/page/<int:page_num>', methods=['GET'])
def get_items2(page_num):
    """
    返回部分物品信息
    :return:
    """
    try:
        data = Item.get_items_page(page_num)
        print(data)
        return dict(code=1, msg='get a part of item data successfully', data=data)
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '返回部分物品信息'


@item.route('/<int:item_id>', methods=['GET'])
def return_item(item_id):
    """
    根据物品id得到物品的信息
    :param item_id: 物品id
    :return:
    """
    try:
        data = Item.get_item(item_id)
        return dict(code=1, msg='get a item data successfully', data=data)
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '返回某个物品信息'


@item.route('/<int:user_id>', methods=['POST'])
def post_item(user_id):
    """
    提交物品信息
    :param user_id:
    :return:
    """
    try:
        req = Transfer()
        data = req.handle_post()
        print('data: ', data)
        u = User.query.get(user_id)
        if Item.create_item(data, u):
            return PostSuccess()
    except Exception as e:
        print(e)
        return UserNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '发布物品信息'


@item.route('/<int:item_id>', methods=['PUT'])
def edit_item(item_id):
    """
    更新item
    :param item_id:
    :return:
    """
    try:
        i = Item.query.get(item_id)
        transfer = Transfer()
        data = transfer.handle_post()
        print('edit_item', data)
        if i.edit_item(data):
            return UpdateSuccess()
        else:
            return UpdateFail()
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '修改物品信息'


@item.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    删除item
    :param item_id:
    :return:
    """
    try:
        i = Item.query.get(item_id)
        i.delete()
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    else:
        return DeleteSuccess()
    # return '删除物品信息'


@item.route('/search', methods=['GET'])
def search_item():
    """
    搜索item get实现
    参数:
        search_key: 指定搜索关键字
        page_num: 指定返回页数(0开始)
    :return:
    """
    try:
        args = Transfer().handle_get()
        search_key = args.get("search_key")
        page_num = int(args.get("page_num"))
        search_key = '%{}%'.format(search_key)
        print("key and page_num: ", search_key, page_num)
        data = Item.search_item(search_key, page_num)
        print(data)
        return dict(code=1, msg='search items successfully', data=data)
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '搜索物品信息'


@item.route('/search', methods=['POST'])
def search_item2():
    """
    搜索item post实现
    参数:
        search_key: 指定搜索关键字
        page_num: 指定返回页数(0开始)
    :return:
    """
    try:
        data = Transfer().handle_post()
        key = '%{}%'.format(data["search_key"])
        page_num = int(data["page_num"])
        print("key and page_num: ", key, page_num)
        data = Item.search_item(key, page_num)
        print(data)
        return dict(code=1, msg='search items successfully', data=data)
    except Exception as e:
        print(e)
        return ItemNotFound() if isinstance(e, NotFound) else SomethingError()
    # return '搜索物品信息'


@item.route('/upload_img', methods=['POST'])
def upload_img():
    """
    上传图片，返回图片地址
    :return: 图片地址
    """
    try:
        print(request.files)
        file = Transfer().handle_file()
        if file and allowed_file(file.filename):
            data = save_upload_img(file, file.filename)
            return dict(code=1, msg='upload img successfully', data=data)
        else:
            return ParameterException()
    except Exception as e:
        print(e)
    except FileNameException:
        return FileNameException()
    except ChoiceImgException:
        return ChoiceImgException()
    except ImgLargeException:
        return ImgLargeException()
    return SomethingError()
    # return "图片地址"


