#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
from enum import Enum, auto
import yaml


#--------------------------------------------------------------------------------
# 애플리케이션 실행 방식.
#--------------------------------------------------------------------------------
class ApplicationExecuteType(Enum):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	UNKNOWN = auto()
	SOURCE = auto()
	BUILD = auto()
	SERVICE = auto()


	#--------------------------------------------------------------------------------
	# 열거체의 요소 값을 요소 이름으로 변경.
	#--------------------------------------------------------------------------------
	@staticmethod
	def ToName(applicationExecuteType : ApplicationExecuteType) -> str:
		return applicationExecuteType.name.upper()


	#--------------------------------------------------------------------------------
	# 요소 이름을 열거체의 요소 값으로 변경.
	#--------------------------------------------------------------------------------
	@staticmethod
	def ToValue(applicationExecuteTypeName : str) -> ApplicationExecuteType:
		try:
			applicationExecuteTypeNameUpper = applicationExecuteTypeName.upper()
			return ApplicationExecuteType[applicationExecuteTypeNameUpper]
		except Exception as exception:
			raise ValueError(applicationExecuteTypeNameUpper)

	#--------------------------------------------------------------------------------
	# YAML을 역직렬화하여 인스턴스 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def YAMLConstrcutor(loader : yaml.Loader, node : yaml.Node) -> ApplicationExecuteType:
		sequences : list = loader.construct_sequence(node, deep = True)		
		return ApplicationExecuteType(sequences[0])