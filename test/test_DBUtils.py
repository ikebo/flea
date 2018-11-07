# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/7
import pymysql
from DBUtils.PooledDB import PooledDB
from flask import Flask

POOL = PooledDB(
    creator=pymysql,    # 使用链接数据库的模块
    maxconnections=6,   # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,        # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,        # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,      # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,      # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],      # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,             # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host='127.0.0.1',
    port=3306,
    user='root',
    password='root',
    database='test',
    charset='utf8'
)


# SQL相关操作写这里面 -> 增删改查
class SQLHelper(object):
    def __init__(self):
        self.conn = POOL.connection()
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def fetch_one(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        self.close()

        return result

    def fetch_all(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        self.close()

        return result


app = Flask(__name__)


@app.route("/")
def hello():
    obj = SQLHelper()
    result = obj.fetch_all('select * from users', [])
    print(result)
    return 'hello world'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)