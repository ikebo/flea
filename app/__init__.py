import os

from flask import Flask, jsonify
from werkzeug.wrappers import Response

app = Flask(__name__)

from app.models import db
from app.admin import admin as admin_blueprint
from app.api.v1 import create_blueprint_api_v1


class JSONResponse(Response):
    """
        可直接返回dict,tuple or list 自动转成json
        所有返回值最终为以下格式:
        {
           code: (0 or 1 or 2) <1表示成功， 0表示正常失败，2表示有异常>
           msg: <提示信息>
           data: <需要返回的数据，格式为dict, 没有可不填>
        }
        但是每次这样返回很繁琐，所在重写了app.response_class 可直接返回dict, tuple or list,
        若为dict, 则格式为:
            return dict(code=.., msg=.., data)
        若为tuple, 因flask中直接返回 a, b, c格式的话会自动调用make_response， 故格式为:
            return (code, msg, data<没有可不填，默认为None>), status_code, headers
        若为list, 格式为:
            return [code, msg, data<没有可不填，默认为None>]
    """

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        if isinstance(rv, tuple) or isinstance(rv, list):
            res = dict(code=rv[0], msg=rv[1], data=rv[2] if len(rv) > 2 else None)
            rv = jsonify(res)
        return super(JSONResponse, cls).force_type(rv, environ)


app.response_class = JSONResponse

app.config.from_object('app.settings')

# 实例化db, 此时app还未启动，需要手动启动程序上下文
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/flea')
def flea():
    return 'Hello Flea!'


@app.route('/flea/static/uploads/<path>/<uri>')
def get_image(path, uri):
    sep = os.path.sep
    uri = path + sep + uri
    print('uri ', uri)
    imgPath = os.path.abspath('.') + sep + 'app' + sep + 'static' + sep + 'uploads' + sep
    imgPath = imgPath + uri
    print('imgPath ', imgPath)
    mdict = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif'
    }
    mime = mdict[((uri.split(sep)[1]).split('.')[1])]
    print('mime ', mime)
    if not os.path.exists(imgPath):
        return (0, 'image does not exists'), 404
    with open(imgPath, 'rb') as f:
        image = f.read()
    return Response(image, mimetype=mime)


app.register_blueprint(admin_blueprint, url_prefix="/flea/admin")
app.register_blueprint(create_blueprint_api_v1(), url_prefix='/flea/api/v1')
