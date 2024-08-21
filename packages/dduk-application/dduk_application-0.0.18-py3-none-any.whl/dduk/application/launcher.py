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
from .internaldata import InternalData as ApplicationData
from .application import Application
from .preparer import EMBEDDEDDATANAME


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
# 실행자 클래스.
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
		# 포함 시킨 정보 파일 불러오기.
		self.__embeddedData = None
		if EMBEDDEDDATANAME in sys.modules:
			self.__embeddedData = sys.modules[EMBEDDEDDATANAME]

		self.__embeddedData.Name = self.__embeddedData.Name
		self.__application = Application(self.__embeddedData.Name)

	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	def Launch(self) -> int:
		builtins.print("__LAUNCH__")

		#--------------------------------------------------------------------------------
		# 빌드 여부 판단.
		isBuild : bool = Launcher.VerifyBuild()
		self.__application.InternalData.SetBuild(isBuild)
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
			self.__application.InternalData.SetExecuteFileName(executeFileName)
			sys.argv = sys.argv[1:]


		#--------------------------------------------------------------------------------
		# 경로 설정.
		self.__application.InternalData.SetRootPath(rootPath)
		self.__application.InternalData.SetSourcePath(sourcePath)
		self.__application.InternalData.SetResourcePath(resourcePath)
		self.__application.InternalData.SetWorkspacePath(workspacePath)

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
						self.__application.InternalData.SetSymbols(symbolsString)

				# 디버그 모드 설정.
				self.__application.InternalData.SetDebug(False)
			else:
				builtins.print("__NOBUILD__")

				# 심볼 설정.
				# VSCODE로부터 정보 파일 불러오기.
				builtins.print("__SYMBOLS__")

				# 심볼 설정.
				if self.__embeddedData:					
					Application.Logger("__EMBEDDED_DATA__")
					symbols = self.__embeddedData.SYMBOLS
					if symbols:
						symbolsString : str = SLASH.join(symbols)
						self.__application.InternalData.SetSymbols(symbolsString)

				# 디버그 모드 설정.
				Application.Logger("__NODEBUG__")
				useDebug : bool = self.__application.HasSymbol(SYMBOL_DEBUG)
				self.__application.InternalData.SetDebug(useDebug)

			# 로그 설정.
			# 순서 : DEBUG < INFO < WARNING < ERROR < CRITICAL.
			useLog : bool = Application.HasSymbol(SYMBOL_LOG)
			if useLog:
				logPath = self.__application.GetRootPathWithRelativePath("logs")
			self.__application.Logger.Start("dduk-application", 0, useLog, logPath)

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
			if self.__application.IsBuild():
				Application.Logger("__NODEBUG__")
			elif not self.__application.IsDebug():
				Application.Logger("__NODEBUG__")
			else:
				Application.Logger("__DEBUG__")

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
	# 실행 환경 체크 : 바이너리 파일에서 실행했는지 상태 확인.
	# - pyinstaller : FROZEN
	#--------------------------------------------------------------------------------
	@staticmethod
	def VerifyBuild() -> bool:
		try:
			isVerify = builtins.getattr(sys, FROZEN, False)
			return isVerify
		except Exception as exception:
			builtins.print(exception)
			return False


	#--------------------------------------------------------------------------------
	# 실행 환경 체크 : 디버그 세션에 연결 된 상태 확인.
	# - pydevd : PyCharm, 3dsmax
	# - ptvsd : 3dsmax
	# - debugpy : VSCode
	#--------------------------------------------------------------------------------
	@staticmethod
	def VerifyDebug() -> bool:
		try:
			isVerify = debugpy.is_client_connected()
			return isVerify
		except Exception as exception:
			builtins.print(exception)
			return False