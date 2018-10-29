# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/29
from werkzeug.local import LocalStack       # 栈 先进后出
from threading import Thread
import time

my_stack = LocalStack()
my_stack.push(1)
print("in main thread after push, value is: " + str(my_stack.top))      # 1


def worker():
    # 新线程
    print("in new thread before push, value is: " + str(my_stack.top))      # None
    my_stack.push(2)
    print("in new thread after push, value is: " + str(my_stack.top))       # 2


new_t = Thread(target=worker, name="new thread")
new_t.start()
time.sleep(1)

# 主线程
print("finally, in main thread value is: " + str(my_stack.top))     # 1