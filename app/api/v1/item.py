"""
  Created by kebo on 2018/10/16
"""

from . import Redprint

item = Redprint("item")

@item.route('')
def get_item():
    return 'item'