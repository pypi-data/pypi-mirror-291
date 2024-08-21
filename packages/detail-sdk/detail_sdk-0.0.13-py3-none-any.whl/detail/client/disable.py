import threading
from contextlib import ContextDecorator
from typing import Any,Optional,Type
class DisableDetail(ContextDecorator):
	threadlocal=threading.local()
	def __enter__(A):A.threadlocal.disabled=True
	def __exit__(A,exc_type,exc_value,exc_traceback):A.threadlocal.disabled=False
	@classmethod
	def is_disabled(A):return getattr(A.threadlocal,'disabled',False)