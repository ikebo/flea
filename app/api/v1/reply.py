"""
  Created by kebo on 2018/10/16
"""

from . import  Redprint

reply = Redprint("reply")

@reply.route('')
def get_reply():
    return 'reply'