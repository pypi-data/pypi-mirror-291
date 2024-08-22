#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
from .applicationexecutetype import ApplicationExecuteType


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
# 준비된 데이터.
#--------------------------------------------------------------------------------
class PreparedData:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	Name : str
	Type : ApplicationExecuteType
	Symbols : set[str]
	Arguments : list[str]
	StartModuleName : str
	StartFunctionName : str


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, **kwargs : dict) -> None:
		self.Name = str()
		self.Type = ApplicationExecuteType.UNKNOWN
		self.Symbols = set()
		self.Arguments = list()
		self.StartModuleName = str()
		self.StartFunctionName = str()
		
		# 있는 값 다 넣기.
		for argumentKey, value in kwargs.items():
			argumentKeyLower : str = argumentKey.lower()
			for memberKey in self.__dict__.keys():
				memberKeyLower : str = memberKey.lower()
				if argumentKeyLower == memberKeyLower:
					builtins.setattr(self, memberKey, value)