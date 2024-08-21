#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
from collections import deque
from datetime import datetime as DateTime


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY : str = ""
LINEFEED : str = "\n"
COMMAWITHSPACE : str = ", "
SLASH : str = "/"
COLON : str = "."
DOUBLEQUOTATION : str = "\""


#--------------------------------------------------------------------------------
# 전역 변수 목록.
#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
# 값의 타입에 따른 문자열 표시 형식으로 변환.
# - 기본적으로 표준 내장 자료형만 취급. (단, Queue, LifoQueue, PriorityQueue는 제외)
# - 클래스도 취급하지만 데이터 클래스만 지원할 것이기 때문에 공개된 어트리뷰트만 취급. (X)
# - 클래스 아예 취급 안함.
#--------------------------------------------------------------------------------
def GetFormatValueString(originalValue : Any) -> str:
	# 문자열.
	if isinstance(originalValue, str):
		return f"{DOUBLEQUOTATION}{originalValue}{DOUBLEQUOTATION}"
	# 기본 데이터형.
	elif isinstance(originalValue, (int, float, bool)):
		return str(originalValue)
	# 리스트.
	elif isinstance(originalValue, list):
		strings : list[str] = list()
		for attributeValue in originalValue:
			attributeValue = GetFormatValueString(attributeValue)
			strings.append(attributeValue)
		formattedValues = COMMAWITHSPACE.join(strings)
		return f"list([{formattedValues}])"
	# 셋.
	elif isinstance(originalValue, set):
		strings : list[str] = list()
		for attributeValue in originalValue:
			attributeValue = GetFormatValueString(attributeValue)
			strings.append(attributeValue)
		formattedValues = COMMAWITHSPACE.join(strings)
		return f"set([{formattedValues}])"
	# 튜플.
	elif isinstance(originalValue, tuple):
		strings : list[str] = list()
		for attributeValue in originalValue:
			attributeValue = GetFormatValueString(attributeValue)
			strings.append(attributeValue)
		formattedValues = COMMAWITHSPACE.join(strings)
		return f"tuple([{formattedValues}])"
	# 프로즌셋.
	elif isinstance(originalValue, frozenset):
		strings : list[str] = list()
		for attributeValue in originalValue:
			attributeValue = GetFormatValueString(attributeValue)
			strings.append(attributeValue)
		formattedValues = COMMAWITHSPACE.join(strings)
		return f"frozenset([{formattedValues}])"
	# 덱.
	elif isinstance(originalValue, deque):
		strings : list[str] = list()
		for attributeValue in originalValue:
			attributeValue = GetFormatValueString(attributeValue)
			strings.append(attributeValue)
		formattedValues = COMMAWITHSPACE.join(strings)
		return f"deque([{formattedValues}])"
	# 딕셔너리.
	elif isinstance(originalValue, dict):
		strings : list[str] = list()
		for attributeName, attributeValue in originalValue.items():
			attributeName = GetFormatValueString(attributeName)
			attributeValue = GetFormatValueString(attributeValue)
			strings.append(f"{attributeName} : {attributeValue}")
		formattedValues = COMMAWITHSPACE.join(strings)
		return f"dict({{{formattedValues}}})"
	# 그 외는 제외.
	else:
		return EMPTY
	

#--------------------------------------------------------------------------------
# 코드 제너레이터 클래스.
#--------------------------------------------------------------------------------
class PYSONGenerator:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__writelines : list[str]
	__processedIdentifiers : set[int]


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__writelines = list()
		self.__processedIdentifiers = set()


	#--------------------------------------------------------------------------------
	# 초기화.
	#--------------------------------------------------------------------------------
	def Clear(self) -> None:
		self.__writelines.clear()
		self.__processedIdentifiers.clear()


	#--------------------------------------------------------------------------------
	# 작성.
	#--------------------------------------------------------------------------------
	def Write(self, text : str) -> None:
		self.__writelines.append(text)


	#--------------------------------------------------------------------------------
	# 제목 주석 작성.
	#--------------------------------------------------------------------------------
	def WriteTitleComment(self, content : str) -> None:
		self.WriteLineComment()
		self.WriteComment(content)
		self.WriteLineComment()


	#--------------------------------------------------------------------------------
	# 주석 작성.
	#--------------------------------------------------------------------------------
	def WriteComment(self, content : str) -> None:
		self.Write(f"# {content}")


	#--------------------------------------------------------------------------------
	# 수평선 주석 작성.
	#--------------------------------------------------------------------------------
	def WriteLineComment(self) -> None:
		self.WriteComment("--------------------------------------------------------------------------------")


	#--------------------------------------------------------------------------------
	# 헤더 작성.
	#--------------------------------------------------------------------------------
	def WriteHeader(self) -> None:
		nowDateTime = DateTime.now()
		self.WriteLineComment()
		self.WriteComment(f"This code was automatically generated.")
		self.WriteComment(f"Created time : {nowDateTime}")
		self.WriteLineComment()
		self.Write(EMPTY)
		self.Write(EMPTY)


	#--------------------------------------------------------------------------------
	# 본문 작성.
	# - 변수를 이름(대문자) = 값 형태로 저장.
	# - 만약 대상이 클래스 일 경우 재귀하여 값을 기반으로 끝까지 파고들어 출력.
	# - 이 경우 AnonymousClass 를 사용하여 할당 후 점기반으로 멤버 추가.
	#--------------------------------------------------------------------------------
	def WriteBodyRecursive(self, variableName : str, variableValue : Any) -> bool:

		# 객체이름이 없을 경우.
		if not variableName:
			return False

		# 객체가 없을 경우.
		if not variableValue:
			return False
		
		# 타입 객체일 경우.
		if isinstance(variableValue, type):
			return False
		
		# 함수 객체일 경우.
		if callable(variableValue):
			return False
		
		# 처리된 객체일 경우.
		identifier : int = builtins.id(variableValue)
		if identifier in self.__processedIdentifiers:
			return False
		
		self.__processedIdentifiers.add(identifier)
		builtins.print(f"{variableName} = {variableValue}")
	
		# 대문자 이름.
		variableNameUpper = variableName.upper()

		# 클래스 인스턴스 일 때.
		if hasattr(variableValue, "__dict__"):
			# 속성 추가가 가능한 무명 클래스 생성.
			self.Write(f"{variableNameUpper} = AnonymousClassType()")

			# 루프를 돌면서 멤버 변수를 작성.
			for attributeName, attributeValue in variableValue.__dict__.items():
				attributeName = cast(str, attributeName)
				if attributeName.startswith("_"):
					continue

				# 이름 결합 하여 본문 작성 추가.
				newVariableNameUpper = f"{variableNameUpper}.{attributeName}"
				self.WriteBodyRecursive(newVariableNameUpper, attributeValue)

		# 일반 변수.
		else:
			variableValue = GetFormatValueString(variableValue)
			self.Write(f"{variableNameUpper} = {variableValue}")

		return True


	#--------------------------------------------------------------------------------
	# 코드 생성.
	#------------------------------------------------------------------------------
	def Generate(self, variableName : str, variableValue : Any) -> str:
		self.Clear()
		self.WriteHeader()
		self.Write(EMPTY)
		self.Write(EMPTY)
		self.WriteTitleComment("참조 모듈 목록.")
		self.Write("from dduk.core.anonymousclass import AnonymousClass")
		self.Write(EMPTY)
		self.Write(EMPTY)
		self.WriteBodyRecursive(variableName, variableValue)
		return LINEFEED.join(self.__writelines)