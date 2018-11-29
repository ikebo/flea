import os
from app import app

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:runtu13..@127.0.0.1:3306/flea"

SESSION_API = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'

APP_ID = 'wx9bf2875ffa3566bb'
APP_SECRET = '448b79549670f89e3b4fe1ac1414bad7'


SECRET_KEY = 'whxy_flea'

UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'png', 'gif'}

ADVICE_PATH = os.path.join(app.static_folder, 'advice')

# 最大 1M
MAX_CONTENT_LENGTH = 1 * 1024 * 1024


