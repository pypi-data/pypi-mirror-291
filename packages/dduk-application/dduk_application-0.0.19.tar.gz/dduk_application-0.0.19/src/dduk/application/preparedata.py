#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
import inspect
import json
import os
from dduk.core.project import Project
from dduk.core.node import Node
from dduk.utility import strutility
from dduk.utility import jsonutility
from .applicationexecutetype import ApplicationExecuteType
from .pysongenerator import PYSONGenerator


#--------------------------------------------------------------------------------
# 준비 데이터.
#--------------------------------------------------------------------------------
class PrepareData:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	Name : str
	Type : ApplicationExecuteType
	Symbols : set[str]
	Arguments : list[str]


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.Name = str()
		self.Type = ApplicationExecuteType.UNKNOWN
		self.Symbols = set()
		self.Arguments = list()
