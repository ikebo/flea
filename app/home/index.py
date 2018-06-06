from . import home
from flask import redirect, url_for, render_template


@home.route('/')
def index():
    return render_template("home/index.html")

@home.route('/hello')
def hello():
    return 'Hello World!'

# @home.route('/signin', method=['GET'])
# # def signin():
# #     return '''
#         <form action=''>
#     '''