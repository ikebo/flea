"""
  Created by kebo on 2018/10/16
"""

from . import Redprint

user = Redprint("user")


@user.route('')
def get_user():
    return 'user'
