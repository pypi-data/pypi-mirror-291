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
from dduk.utility import jsonutility
from .applicationexecutetype import ApplicationExecuteType
from .prepareddata import PreparedData


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
PREPARED_DATANAME : str = "__prepared_data__"
PREPARED_DATAFILENAME : str = f"{PREPARED_DATANAME}.py"
BACKSLASH : str = "\\"
SLASH : str = "/"
COLON : str = "."
PYEXTENSION : str = ".py"
PACKAGE : str = "PACKAGE"
MODULE : str = "MODULE"
CLASS : str = "CLASS"
FUNCTION : str = "FUNCTION"
CARRIAGERETURN : str = "\r"
EMPTY : str = ""
LINEFEED : str = "\n"
READ : str = "r"
WRITE : str = "w"
UTF8 : str = "utf-8"
ASTERISK : str = "*"
DOUBLEQUOTATION : str = "\""
DDUK : str = "dduk"
APPLICATION : str = "application"

SOURCE : str = "source"
BUILD : str = "build"
SERVICE : str = "service"

SYMBOLS : str = "symbols"
ARGUMENTS : str = "Arguments"


#--------------------------------------------------------------------------------
# 준비자 클래스.
# - 데이터를 파이썬 코드로 변형해서 저장하므로 이후 추가 비용 없이 파일 이름만 알고 있으면 불러와 사용 가능.
# - 단, 이미 모듈이 리로드 되었다는 전제.
#--------------------------------------------------------------------------------
class Preparer:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 준비.
	#--------------------------------------------------------------------------------
	def Prepare(self, applicationExecuteType : ApplicationExecuteType) -> None:
		# 호출 스택 조사.
		stack = inspect.stack()
		if len(stack) < 2:
			raise Exception("Inspector Exception.")
		
		# 루트 경로와 루트 이름 생성.
		currrentFrame = inspect.stack()[1]
		startFilePath =  currrentFrame.filename
		rootPath = Project.FindRootPath(startFilePath)
		rootPath = rootPath.replace(BACKSLASH, SLASH)
		rootName = os.path.basename(rootPath)
		rootName = rootName.lower()
		
		# 파일 경로 생성.
		prepareFilePath : str = f"{rootPath}/src/{PREPARED_DATAFILENAME}"

		# 기존 파일 제거.
		if os.path.exists(prepareFilePath):
			os.remove(prepareFilePath)

		# 새로운 데이터 만들기.
		prepareData = PreparedData()
		prepareData.Name = rootName
		prepareData.Type = applicationExecuteType

		# 비주얼 스튜디오 코드로부터 셋팅 가져오기.
		settings : dict = self.GetVisualStudioCodeSettings(rootPath, prepareData.Type)
		if settings:
			if SYMBOLS in settings:
				prepareData.Symbols.clear()
				symbols : list[str] = settings[SYMBOLS]
				symbols : list[str] = [symbol.upper() for symbol in symbols]
				prepareData.Symbols.update(symbols)

			if prepareData.Type == ApplicationExecuteType.SOURCE:
				if ARGUMENTS in settings:
					arguments : list[str] = settings[ARGUMENTS]
					prepareData.Arguments.clear()
					prepareData.Arguments.extend(arguments)
					builtins.print(arguments)

		# 코드 생성.
		content = str()
		content += "from dduk.application.prepareddata import PreparedData"
		content += "from dduk.application.applicationexecutetype import ApplicationExecuteType"
		content += ""
		content += ""
		content += repr(prepareData)

		# 파일 기록.
		with open(prepareFilePath, WRITE, encoding = UTF8) as file:
			file.write(content)
			builtins.print(content)


	#--------------------------------------------------------------------------------
	# .vscode/settings.json 파일에서 상황에 맞는 데이터 가져오기.
	#--------------------------------------------------------------------------------
	def GetVisualStudioCodeSettings(self, rootPath : str, applicationExecuteType : ApplicationExecuteType) -> dict:
		try:
			vscodeSettingsFilePath = f"{rootPath}/.vscode/settings.json"
			if not os.path.exists(vscodeSettingsFilePath):
				return dict()
			with builtins.open(vscodeSettingsFilePath, READ, encoding = UTF8) as file:
				string = file.read()
				jsonText = jsonutility.RemoveAllCommentsInString(string)
				vscodeSettings = json.loads(jsonText)
		except Exception as exception:
			builtins.print(exception)
			return dict()
		
		try:
			if not vscodeSettings:
				raise ValueError("settings.json")
			if DDUK not in vscodeSettings:
				raise ValueError(DDUK)

			ddukSettings = vscodeSettings[DDUK]
			if APPLICATION not in vscodeSettings:
				raise ValueError(APPLICATION)

			applicationSettings = ddukSettings[APPLICATION]

			# 소스 모드 설정.
			if applicationExecuteType == ApplicationExecuteType.SOURCE:
				if SOURCE in applicationSettings:
					return applicationSettings[SOURCE]
				else:
					raise ValueError(SOURCE)
			# 빌드 모드 설정.
			elif applicationExecuteType == ApplicationExecuteType.BUILD:
				if BUILD in applicationSettings:
					return applicationSettings[BUILD]
				else:
					raise ValueError(BUILD)
			# 서비스 모드 설정.
			elif applicationExecuteType == ApplicationExecuteType.SERVICE:
				if SERVICE in applicationSettings:
					return applicationSettings[SERVICE]
				else:
					raise ValueError(SERVICE)
		except Exception as exception:
			builtins.print(exception)
			return dict()		