#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
from enum import Enum, auto
import json
import os
from dduk.core.project import Project
from dduk.core.node import Node
from dduk.utility import strutility
from dduk.utility import jsonutility
from .pysongenerator import PYSONGenerator


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMBEDDEDDATANAME : str = "__embeddeddata__"
EMBEDDEDDATAFILENAME : str = f"{EMBEDDEDDATANAME}.py"
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
DEFAULT_REMOTEDEBUGPORT : int = 4885
DEFAULT_EMBEDDEDDATANAME : str = "EMBEDDEDDATA"

DDUK : str = "dduk"
APPLICATION : str = "application"
DEBUG : str = "debug"
NODEBUG : str = "nodebug"
BUILD : str = "build"
SERVICE : str = "service"

EMBEDMODE : str = "embedMode"
REMOTEPORT : str = "remotePort"
SYMBOLS : str = "symbols"
ARGUMENTS : str = "Arguments"



#--------------------------------------------------------------------------------
# 임베딩 실행 모드.
#--------------------------------------------------------------------------------
class EmbeddingExecuteMode(Enum):
	DEBUG = auto()
	NODEBUG = auto()
	BUILD = auto()
	SERVICE = auto()

	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	@staticmethod
	def ToName(embeddingExecuteMode : EmbeddingExecuteMode) -> str:
		return embeddingExecuteMode.name.upper()

	@staticmethod
	def ToValue(embeddingExecuteMode : str) -> EmbeddingExecuteMode:
		try:
			embeddingExecuteMode = embeddingExecuteMode.upper()
			return EmbeddingExecuteMode[embeddingExecuteMode]
		except Exception as exception:
			raise ValueError(embeddingExecuteMode)
		

#--------------------------------------------------------------------------------
# 내장 하려고 하는 데이터.
#--------------------------------------------------------------------------------
class EmbeddingData:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	Name : str
	IsDebug : int
	RemoteDebugPort : int
	Symbols : set[str]
	Arguments : list[str]


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.Name = str()
		self.IsDebug = False
		self.RemoteDebugPort = DEFAULT_REMOTEDEBUGPORT
		self.Symbols = set()
		self.Arguments = list()


#--------------------------------------------------------------------------------
# 데이터 내장 처리기 클래스.
# - 데이터를 파이썬 코드로 변형해서 저장하므로 이후 추가 비용 없이 파일 이름만 알고 있으면 불러와 사용 가능.
# - 단, 이미 모듈이 리로드 되었다는 전제.
#--------------------------------------------------------------------------------
class Embedder:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 데이터를 코드로 만들어 저장.
	#--------------------------------------------------------------------------------
	def Embed(self, sourcePath : str, embeddingExecuteMode : EmbeddingExecuteMode) -> None:
		
		# 파일 경로 생성.
		embeddedDataFilePath : str = f"{sourcePath}/{EMBEDDEDDATAFILENAME}"

		# 기존 파일 제거.
		if os.path.exists(embeddedDataFilePath):
			os.remove(embeddedDataFilePath)

		# 루트 경로와 루트 이름 생성.
		rootPath = Project.FindRootPath(sourcePath)
		rootPath = rootPath.replace(BACKSLASH, SLASH)
		rootName = os.path.basename(rootPath)
		rootName = rootName.lower()

		# 새로운 데이터 만들기.
		embeddingData = EmbeddingData()
		embeddingData.Name = rootName
		embeddingData.IsDebug = embeddingExecuteMode == EmbeddingExecuteMode.DEBUG

		# 비주얼 스튜디오 코드로부터 셋팅 가져오기.
		settings : dict = self.GetVisualStudioCodeSettingsByExecutionMode(embeddingExecuteMode)
		if settings:
			if REMOTEPORT in settings:
				embeddingData.RemoteDebugPort = settings[REMOTEPORT]

			if SYMBOLS in settings:
				embeddingData.Symbols.clear()
				symbolsString = settings[SYMBOLS]
				symbolsString = symbolsString.upper()
				symbols : list[str] = strutility.GetStringFromSeperatedStringList(symbolsString, SLASH)
				embeddingData.Symbols.update(symbols)

			if ARGUMENTS in settings:
				embeddingData.Arguments.clear()
				argumentsString = settings[ARGUMENTS]
				builtins.print(argumentsString)
				embeddingData.Arguments.extend(argumentsString)


		# 코드 생성.
		builtins.print("__EMBED__START__")
		pysonGenerator = PYSONGenerator()
		content = pysonGenerator.Generate(DEFAULT_EMBEDDEDDATANAME, embeddingData)
		builtins.print("__EMBED__END__")

		# 파일 기록.
		with open(embeddedDataFilePath, WRITE, encoding = UTF8) as file:
			file.write(content)
			builtins.print(content)


	#--------------------------------------------------------------------------------
	# .vscode/settings.json 파일 불러오기.
	#--------------------------------------------------------------------------------
	def GetVisualStudioCodeSettings(self, rootPath : str) -> dict:
		try:
			vscodeSettingsFilePath = f"{rootPath}/.vscode/settings.json"
			if not os.path.exists(vscodeSettingsFilePath):
				return dict()
			with builtins.open(vscodeSettingsFilePath, READ, encoding = UTF8) as file:
				string = file.read()
				jsonText = jsonutility.RemoveAllCommentsInString(string)
				vscodeSettings = json.loads(jsonText)
				return vscodeSettings			
		except Exception as exception:
			builtins.print(exception)
			return dict()


	#--------------------------------------------------------------------------------
	# .vscode/settings.json 파일에서 상황에 맞는 데이터 가져오기.
	#--------------------------------------------------------------------------------	
	def GetVisualStudioCodeSettingsByExecutionMode(self, rootPath : str, executeMode : EmbeddingExecuteMode) -> dict:
		vscodeSettingsFilePath = f"{rootPath}/.vscode/settings.json"
		vscodeSettings = self.GetVisualStudioCodeSettings(rootPath)
		if not vscodeSettings:
			raise ValueError(vscodeSettingsFilePath)
		if DDUK not in vscodeSettings:
			raise ValueError(DDUK)

		ddukSettings = vscodeSettings[DDUK]
		if APPLICATION not in vscodeSettings:
			raise ValueError(APPLICATION)

		applicationSettings = ddukSettings[APPLICATION]

		# 디버그 모드 설정.
		if executeMode == EmbeddingExecuteMode.DEBUG:
			if DEBUG in applicationSettings:
				return applicationSettings[DEBUG]
			else:
				raise ValueError(DEBUG)
		# 노디버그 모드 설정.
		elif executeMode == EmbeddingExecuteMode.NODEBUG:
			if NODEBUG in applicationSettings:
				return applicationSettings[NODEBUG]
			else:
				raise ValueError(NODEBUG)
		# 빌드 모드 설정.
		elif executeMode == EmbeddingExecuteMode.BUILD:
			if BUILD in applicationSettings:
				return applicationSettings[BUILD]
			else:
				raise ValueError(BUILD)
		# 서비스 모드 설정.
		elif executeMode == EmbeddingExecuteMode.SERVICE:
			if SERVICE in applicationSettings:
				return applicationSettings[SERVICE]
			else:
				raise ValueError(SERVICE)