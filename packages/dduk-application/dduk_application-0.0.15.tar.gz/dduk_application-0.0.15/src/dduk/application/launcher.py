#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
import importlib
import os
import signal
import sys
from types import ModuleType
import debugpy
from dduk.core.repository import Repository
from .data import Data as ApplicationData
from .application import Application
from .embedder import EMBEDDEDDATANAME


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY : str = ""
FROZEN : str = "frozen"
MAIN : str = "__main__"
BACKSLASH : str = "\\"
SLASH : str = "/"
# CURRENTFILEPATH : str = os.path.abspath(__file__)
# SRCPATH : str = os.path.dirname(CURRENTFILEPATH).replace(BACKSLASH, SLASH)
SYMBOL_SUBPROCESS : str = "SUBPROCESS"
SYMBOL_LOG : str = "LOG"
SYMBOL_DEBUG : str = "DEBUG"
SYMBOL_NODEBUG : str = "NODEBUG"


#--------------------------------------------------------------------------------
# 실행 처리기 클래스.
#--------------------------------------------------------------------------------
class Launcher:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__application : Application
	__embeddedData : ModuleType


	#--------------------------------------------------------------------------------
	# 애플리케이션 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def Application(self) -> Application:
		return self.__application
	

	#--------------------------------------------------------------------------------
	# 임베디드 모듈 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def Embedded(self) -> ModuleType:
		return self.__embeddedData
	

	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__application = Application()
		self.__embeddedData = None

		# 포함 시킨 정보 파일 불러오기.
		if EMBEDDEDDATANAME in sys.modules:
			self.__embeddedData = sys.modules[EMBEDDEDDATANAME]


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	def Launch(self) -> int:
		builtins.print("__LAUNCH__")

		#--------------------------------------------------------------------------------
		# 빌드 여부 판단.
		isBuild : bool = IsBuild()
		self.__application.Data.SetBuild(isBuild)
		if isBuild:
			# 실행파일에서 생성되는 임시 루트 경로.
			# 리소스를 위한 캐시폴더로 실제 실행파일의 위치가 아님.
			cachePath : str = sys._MEIPASS.replace(BACKSLASH, SLASH)
			rootPath : str = os.path.dirname(sys.executable).replace(BACKSLASH, SLASH)
			sourcePath : str = os.path.join(cachePath, "src").replace(BACKSLASH, SLASH)
			resourcePath : str = os.path.join(cachePath, "res").replace(BACKSLASH, SLASH)
			workspacePath : str = rootPath.replace(BACKSLASH, SLASH)
		else:
			# 현재 __main__ 으로 실행되는 코드 대상을 기준으로 한 경로.
			# 따라서 반드시 메인 스크립트는 src 안에 있어야 한다.
			currentFilePath = os.path.abspath(sys.modules[MAIN].__file__).replace(BACKSLASH, SLASH)
			sourcePath : str = os.path.dirname(currentFilePath) .replace(BACKSLASH, SLASH)
			rootPath : str = os.path.dirname(sourcePath).replace(BACKSLASH, SLASH)
			resourcePath : str = os.path.join(rootPath, "res").replace(BACKSLASH, SLASH)
			workspacePath : str = os.path.join(rootPath, "workspace").replace(BACKSLASH, SLASH)


		#--------------------------------------------------------------------------------
		# 실행 인수 : 실행된 파일 이름 설정.
		if sys.argv:
			Application.Logger("__EXECUTE__")
			executeFileName = sys.argv[0]
			self.__application.Data.SetExecuteFileName(executeFileName)
			sys.argv = sys.argv[1:]


		#--------------------------------------------------------------------------------
		# 경로 설정.
		self.__application.Data.SetRootPath(rootPath)
		self.__application.Data.SetSourcePath(sourcePath)
		self.__application.Data.SetResourcePath(resourcePath)
		self.__application.Data.SetWorkspacePath(workspacePath)

		#--------------------------------------------------------------------------------
		# 경로 출력.
		builtins.print(f"isBuild: {self.__application.IsBuild()}")
		builtins.print(f"rootPath: {self.__application.GetRootPath()}")
		builtins.print(f"isBuild: {self.__application.IsBuild()}")
		builtins.print(f"sourcePath: {self.__application.GetSourcePath()}")
		builtins.print(f"resourcePath: {self.__application.GetResourcePath()}")
		builtins.print(f"workspacePath: {self.__application.GetWorkspacePath()}")

		#--------------------------------------------------------------------------------
		# 심볼 및 로그 설정.
		try:
			if isBuild:
				builtins.print("__BUILD__")

				# 심볼 설정.
				if self.__embeddedData:					
					Application.Logger("__EMBEDDED_DATA__")
					symbols = self.__embeddedData.SYMBOLS
					if symbols:
						symbolsString : str = SLASH.join(symbols)
						self.__application.Data.SetSymbols(symbolsString)

				# 디버그 모드 설정.
				self.__application.Data.SetDebug(False)
			else:
				builtins.print("__NOBUILD__")

				# 심볼 설정.
				# VSCODE로부터 정보 파일 불러오기.
				builtins.print("__SYMBOLS__")

				# # 배치파일을 통한 실행시 9개 중 7개의 미사용 인수가 넘어오므로.
				# # 심볼의 경우 첫글자는 영어대문자 혹은 언더바여야 하고, 이후는 영어대문자, 언더바, 숫자가 조합될 수 있음. 띄어쓰기 등은 허용하지 않음.
				# sys.argv = [argument for argument in sys.argv if argument]
				# symbolsString = sys.argv[0]
				# self.__application.Data.SetSymbols(symbolsString)
				# sys.argv = sys.argv[1:]

				# 심볼 설정.
				if self.__embeddedData:					
					Application.Logger("__EMBEDDED_DATA__")
					symbols = self.__embeddedData.SYMBOLS
					if symbols:
						symbolsString : str = SLASH.join(symbols)
						self.__application.Data.SetSymbols(symbolsString)


				# 디버그 모드 설정.
				Application.Logger("__NODEBUG__")
				useDebug : bool = self.__application.HasSymbol(SYMBOL_DEBUG)
				self.__application.Data.SetDebug(useDebug)

			# 로그 설정.
			# 순서 : DEBUG < INFO < WARNING < ERROR < CRITICAL.
			useLog : bool = Application.HasSymbol(SYMBOL_LOG)
			if useLog:
				logPath = self.__application.GetRootPathWithRelativePath("logs")
			self.__application.Logger.Run("dduk-application", 0, useLog, logPath)

		except Exception as exception:
			builtins.print(exception)

		# # 시그널 등록.
		# signal.signal(signal.SIGINT, lambda sight, frame: sys.exit(0))

		#--------------------------------------------------------------------------------
		# 공통 : 인자 및 디버그 설정 및 시작.
		try:
			# sys.argv = CreateStringListFromSeperatedStringList(sys.argv)
			# 잔여 인자 출력.
			if sys.argv:
				Application.Logger("__ARGUMENTS__")
				index = 0
				for arg in sys.argv:
					Application.Logger(f" - [{index}] {arg}")
					index += 1

			# 디버그 설정.
			if self.__application.isBuild():
				Application.Logger("__NODEBUG__")
			elif not self.__application.IsDebug():
				Application.Logger("__NODEBUG__")
			else:
				Application.Logger("__DEBUG__")
				Application.Logger("dduk.application.debug.start()")
				if self.__embeddedData:
					remotePort : int = self.__embeddedData.DEBUG_REMOTE_PORT
				else:
					remotePort : int = 4885 # vscodeSettings["launcher"]["debug"]["remotePort"]
				
				# 디버그 파이는 기존 설정을 초기화 할 수는 없고 추가한 설정값으로 덮어쓰기만 가능.
				configuration : dict[str, Any] = dict()
				exceptionOptions : list[dict[str, Any]] = list()
				configuration["exception_options"] = exceptionOptions
				exceptionOption : dict[str, Any]= dict()
				path : list[dict[str, list[str]]] = list()
				pathElement : dict[str, list[str]] = dict()
				pathElementValues : list[str] = list()
				pathElementValues.append("SystemExit")
				pathElement["names"] = pathElementValues
				path.append(pathElement)
				exceptionOption["path"] = path
				exceptionOption["break_mode"] = "never"
				exceptionOptions.append(exceptionOption)
				debugpy.configure(configuration)
				
				debugpy.listen(("localhost", remotePort))
				Application.Logger("dduk.application.debug.wait()")
				debugpy.wait_for_client()
				Application.Logger("dduk.application.debug.started()")

			module : ModuleType = importlib.import_module(self.__embeddedData.START_MODULE_NAME)
			function = builtins.getattr(module, self.__embeddedData.START_FUNCTION_NAME)
			exitCode : int = function(sys.argv)
			return exitCode
		# except KeyboardInterrupt as exception:
		# 	# if self.__application.IsBuild():
		# 	# 	return 0
		# 	# else:
		# 	# 	Application.LogException(exception)
		# 	return 0
		except Exception as exception:
			Application.LogException(exception)


#--------------------------------------------------------------------------------
# 빌드 여부.
#--------------------------------------------------------------------------------
def IsBuild() -> bool:
	# 실행 환경 체크.
	try:
		return builtins.getattr(sys, FROZEN, False)
	except Exception as exception:
		return False