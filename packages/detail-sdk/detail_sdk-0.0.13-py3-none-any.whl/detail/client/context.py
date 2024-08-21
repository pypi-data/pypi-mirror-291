import threading
from typing import Optional
from detail.client import logs
_tlocal=threading.local()
_index=0
_tlock=threading.Lock()
_wsgi_span_id=None
_wsgi_lock=threading.Lock()
logger=logs.get_detail_logger(__name__)
def set_wsgi_span_id(span_id):
	global _wsgi_span_id
	with _wsgi_lock:_wsgi_span_id=span_id
def get_wsgi_span_id():
	global _wsgi_span_id
	with _wsgi_lock:return _wsgi_span_id
def get_thread_index():
	global _index
	if threading.current_thread()is threading.main_thread():return 0
	if not hasattr(_tlocal,'index'):
		with _tlock:_index+=1;_tlocal.index=_index
		logger.info('assigned thread index %s to thread %r (id %s)',_tlocal.index,threading.current_thread().name,threading.get_ident())
	return _tlocal.index