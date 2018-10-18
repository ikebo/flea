# from app import db

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 只有导入Model才会在数据库建表
from . import user
from . import item
from . import comment
from . import reply