from flask import Blueprint

home = Blueprint("home", __name__)

# 只有导入视图函数才会执行那些代码,也就是注册视图函数
import app.home.user
import app.home.index