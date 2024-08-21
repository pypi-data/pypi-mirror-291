from typing import Any,Callable
import forbiddenfruit
from opentelemetry.trace import SpanKind,Tracer
from wrapt.wrappers import _FunctionWrapperBase
from detail.client import stack
from detail.client.attrs import build_pure_attributes,is_active,set_attributes
from detail.client.disable import DisableDetail
from detail.client.logs import get_detail_logger
from detail.client.recursion import RecursionTracker
logger=get_detail_logger(__name__)
def get_pure_wrapper(tracer,library,empty_args=False,kind=SpanKind.INTERNAL):
	E=library
	def A(wrapped,instance,args,kwargs):
		C=kwargs;B=args;A=wrapped
		if DisableDetail.is_disabled():return A(*B,**C)
		D=f"{E}.{A.__qualname__}"
		if RecursionTracker.is_recursing(D):
			with DisableDetail():return A(*B,**C)
		H=stack.get_caller_path()
		if stack.is_ignored_instrumentation_caller(H):
			with DisableDetail():return A(*B,**C)
		with RecursionTracker(D):
			with tracer.start_as_current_span(D,kind=kind)as F:
				G=A(*B,**C)
				if is_active(F):I=build_pure_attributes(E,A.__qualname__,B,C,G,empty_args);set_attributes(F,I)
				return G
	return A
class CopyableFunctionWrapperBase(_FunctionWrapperBase):
	def __copy__(A):return A
	def __deepcopy__(A,*B,**C):return A
def force_function_wrapper(target,name,wrapper,binding):C=binding;B=name;A=target;assert C in['function','classmethod','staticmethod'];D=getattr(A,B);E=A;F=getattr(A,'__dict__')[B];G=CopyableFunctionWrapperBase(D,E,wrapper,binding=C,parent=F);forbiddenfruit.curse(A,B,G)