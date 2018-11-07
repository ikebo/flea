"""
    app/api/v1/item.py:
    item相关API
        /api/v1/item/   GET   								返回所有物品信息
        /api/v1/item/page/<int:page_num>   GET              访问部分物品信息 page_num指定返回范围
        /api/v1/item/<int:item_id>   GET   					返回某个物品详细信息
        /api/v1/item/<int: user_id>  POST    				发布物品信息
        /api/v1/item/<int:item_id>   PUT   					修改某个物品信息
        /api/v1/item/<int: item_id>  DELETE   				删除某个物品信息

        /api/v1/item/search	                GET			    搜索物品
        /api/v1/item/upload_img             POST   			上传图片  返回图片地址
"""
from . import Redprint
from app.req_res import *
from app.req_res.res import Res
from app.req_res.transfer import Transfer
from app.utils.file import allowed_file, save_upload_img
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
        items = Item.query.join(User).all()
        if items is None:
            return ItemNotFound()
        data = [i.raw() for i in items]
        print(data)
        return Res(msg='get all item data successfully', data=data).jsonify()
    except Exception as e:
        print(e)
    return SomethingError()
    # return '返回物品信息'


@item.route('/page/<int:page_num>', methods=['GET'])
def get_item2(page_num):
    """
    返回部分物品信息
    :return:
    """
    try:
        query = Item.query.join(User)
        items = query.order_by(Item.time.desc()).offset(page_num * 8).limit(8).all()
        if items is None:
            return ItemNotFound()
        data = [i.raw() for i in items]
        print(data)
        return Res(msg='get a part of item data successfully', data=data).jsonify()
    except Exception as e:
        print(e)
        if isinstance(e, NotFound):
            return NotFound()
    return SomethingError()
    # return '返回部分物品信息'


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
        return Res(code=1, msg='get item successfully', data=data).jsonify()
    except Exception as e:
        print(e)
        if isinstance(e, NotFound):
            return ItemNotFound()
    return SomethingError()
    # return '返回某个物品信息'


@item.route('/<int:user_id>', methods=['POST'])
def post_item(user_id):
    transfer = Transfer()
    data = transfer.handle_post()
    print('data: ', data)
    user = User.query.get(user_id)
    if user is None:
        return UserNotFound()
    if Item.create_item(data, user_id) and user.update_contact(data):
        return PostSuccess()
    return SomethingError()
    # return '发布物品信息'


@item.route('/<int:item_id>', methods=['PUT'])
def edit_item(item_id):
    """
    更新item
    :param item_id:
    :return:
    """
    i = Item.query.get(item_id)
    if i is None:
        return ItemNotFound()
    transfer = Transfer()
    data = transfer.handle_post()
    print('edit_item', data)
    if i.edit(data):
        return EditSuccess()
    return SomethingError()
    # return '修改物品信息'


@item.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    删除item
    :param item_id:
    :return:
    """
    i = Item.query.get(item_id)
    if i is None:
        return ItemNotFound()
    if i.delete():
        return DeleteSuccess()
    else:
        return SomethingError()
    # return '删除物品信息'


@item.route('/search', methods=['GET'])
def search_item():
    """
    搜索item
    :return:
    """
    try:
        page = int(request.args.get('page'))
        search_key = request.args.get('key')
        key = '%{}%'.format(search_key)
        print('key', key)
        query = Item.query.join(User)
        items = query.filter(Item.des.like(key)).order_by(Item.time.desc()).offset(page * 8).limit(8).all()
        data = [i.raw() for i in items]
        print(data)
        return Res(1, 'search items successfully', data).jsonify()
    except Exception as e:
        print(e)
        if isinstance(e, NotFound):
            return NotFound()
    return SomethingError()
    # return '搜索物品信息'


@item.route('/upload_img', methods=['POST'])
def upload_img():
    """
    上传图片，返回图片地址
    :return: 图片地址
    """
    try:
        print(request.files)
        transfer = Transfer()
        file = transfer.handle_file()
        if file and allowed_file(file.filename):
            data = save_upload_img(file, file.filename)
            return Res(1, 'upload img successfully', data).jsonify()
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


