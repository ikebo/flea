from functools import partial
from werkzeug.local import LocalProxy

def _lookup_req_object(name):
	top = _request_ctx_stack.top
	if top is None:
		raise RuntimeError('outside context')
	return getattr(top, name)

request = LocalProxy(partial(_lookup_req_object, 'request'))