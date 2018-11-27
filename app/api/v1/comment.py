"""
  Created by kebo on 2018/10/16
"""

from . import Redprint

comment = Redprint("comment")

@comment.route('')
def get_comment():
    return 'comment'
