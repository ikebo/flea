from flask import Flask, jsonify
from werkzeug.wrappers import Response

app = Flask(__name__)

from app.models import db
from app.admin import admin as admin_blueprint
from app.api.v1 import create_blueprint_api_v1


class JSONResponse(Response):
    """可直接返回dict,tuple or list 自动转成json"""

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

app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(create_blueprint_api_v1(), url_prefix='/api/v1')
