from flask import Flask

app = Flask(__name__)

from app.models import db
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.config.from_object('app.settings')

# 实例化db, 此时app还未启动，需要手动启动程序上下文
db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")
