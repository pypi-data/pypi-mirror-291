import threading
from typing import Any,Optional,Type
class RecursionTracker:
	threadlocal=threading.local()
	def __init__(A,id):A.id=id
	@classmethod
	def is_recursing(A,id):return bool(A.threadlocal.__dict__.get(id,False))
	def __enter__(A):A.threadlocal.__dict__[A.id]=True
	def __exit__(A,exc_type,exc_value,exc_traceback):del A.threadlocal.__dict__[A.id]