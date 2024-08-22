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
import yaml
from dduk.core.repository import Repository
from dduk.core.project import Project
from dduk.utility.logging.logtype import LogType
from .applicationexecutetype import ApplicationExecuteType
from .internaldata import InternalData as ApplicationData
from .application import Application
from .prepareddata import PreparedData
from .predefinedsymbols import SYMBOL_LOG
from .preparer import PREPARED_DATAFILENAME



#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY : str = ""
FROZEN : str = "frozen"
MAIN : str = "__main__"
BACKSLASH : str = "\\"
SLASH : str = "/"
UTF8 : str = "utf-8"
READ : str = "r"
WRITE : str = "w"


#--------------------------------------------------------------------------------
# 실행자 클래스.
#--------------------------------------------------------------------------------
class Launcher:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__application : Application


	#--------------------------------------------------------------------------------
	# 애플리케이션 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def Application(self) -> Application:
		return self.__application


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__application = None


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	def Launch(self) -> int:
		builtins.print("__LAUNCH__")

		#--------------------------------------------------------------------------------
		# 빌드 설정.
		isBuild : bool = Launcher.VerifyBuild()
		if isBuild:
			# 실행파일에서 생성되는 임시 루트 경로.
			# 리소스를 위한 캐시폴더로 실제 실행파일의 위치가 아님.
			# builtins.hasattr(sys, "_MEIPASS")
			cachePath : str = sys._MEIPASS.replace(BACKSLASH, SLASH)
			rootPath : str = os.path.dirname(sys.executable).replace(BACKSLASH, SLASH)
			sourcePath : str = os.path.join(cachePath, "src").replace(BACKSLASH, SLASH)
			resourcePath : str = os.path.join(cachePath, "res").replace(BACKSLASH, SLASH)
			workspacePath : str = rootPath.replace(BACKSLASH, SLASH)
			metaPath : str = os.path.join(cachePath, "meta").replace(BACKSLASH, SLASH)
		else:
			# 현재 __main__ 으로 실행되는 코드 대상을 기준으로 한 경로.
			# 따라서 반드시 메인 스크립트는 src 안에 있어야 한다.
			currentFilePath = os.path.abspath(sys.modules[MAIN].__file__).replace(BACKSLASH, SLASH)
			sourcePath : str = os.path.dirname(currentFilePath) .replace(BACKSLASH, SLASH)
			rootPath : str = os.path.dirname(sourcePath).replace(BACKSLASH, SLASH)
			resourcePath : str = os.path.join(rootPath, "res").replace(BACKSLASH, SLASH)
			workspacePath : str = os.path.join(rootPath, "workspace").replace(BACKSLASH, SLASH)

			# 빌드가 아닌 상태에서의 추가 경로 설정.
			rootName = os.path.basename(rootPath)
			temporaryPath = Project.FindTemporaryPath()
			cachePath : str = os.path.join(temporaryPath, "dduk", "application", "projects", rootName).replace(BACKSLASH, SLASH)
			metaPath : str = os.path.join(cachePath, "meta").replace(BACKSLASH, SLASH)
		
		#--------------------------------------------------------------------------------
		# 프리페어 데이터 파일 로드.
		prepareFilePath : str = f"{metaPath}/{PREPARED_DATAFILENAME}"
		builtins.print(f"prepareFilePath: {prepareFilePath}")
		with open(prepareFilePath, READ, encoding = UTF8) as file:
			yamlString = file.read()
			# yaml.add_constructor("!!python/object:dduk.application.prepareddata.PreparedData", PreparedData.YAMLConstructor)
			# yaml.add_constructor("!!python/object/apply:dduk.application.applicationexecutetype.ApplicationExecuteType", ApplicationExecuteType.YAMLConstructor)
			yaml.add_constructor("tag:yaml.org,2002:python/object:dduk.application.prepareddata.PreparedData", PreparedData.YAMLConstructor)
			yaml.add_constructor("tag:yaml.org,2002:python/object/apply:dduk.application.applicationexecutetype.ApplicationExecuteType", ApplicationExecuteType.YAMLConstructor)			
			
			try:
				preparedData : PreparedData = yaml.load(yamlString, Loader = yaml.FullLoader)
			except Exception as exception:
				builtins.print(f"yaml.load: {exception}")

		#--------------------------------------------------------------------------------
		# 애플리케이션 설정.
		self.__application = Application(preparedData)
		self.__application.InternalData.SetBuild(isBuild)

		#--------------------------------------------------------------------------------
		# 심볼 설정.
		# 준비 데이터로부터 심볼목록을 불러와 설정.
		builtins.print("__PREPARED__")
		self.__application.InternalData.SetSymbols(self.Application.PreparedData.Symbols)

		#--------------------------------------------------------------------------------
		# 디버깅 설정. (서비스와 빌드는 디버깅 할 수 없다고 간주한다.)
		if self.__application.PreparedData.Type == ApplicationExecuteType.SOURCE:
			isDebug : bool = Launcher.VerifyDebug()
			self.__application.InternalData.SetDebug(isDebug)
		else:
			self.__application.InternalData.SetDebug(False)

		#--------------------------------------------------------------------------------
		# 실행 인수 : 실행된 파일 이름 설정.
		if sys.argv:
			builtins.print("__EXECUTE__")
			executeFileName = sys.argv[0]
			self.__application.InternalData.SetExecuteFileName(executeFileName)

		#--------------------------------------------------------------------------------
		# 경로 설정.
		self.__application.InternalData.SetRootPath(rootPath)
		self.__application.InternalData.SetMetaPath(metaPath)
		self.__application.InternalData.SetSourcePath(sourcePath)
		self.__application.InternalData.SetResourcePath(resourcePath)
		self.__application.InternalData.SetWorkspacePath(workspacePath)

		#--------------------------------------------------------------------------------
		# 경로 출력.
		builtins.print(f"isBuild: {self.__application.IsBuild()}")
		builtins.print(f"rootPath: {self.__application.GetRootPath()}")
		builtins.print(f"isBuild: {self.__application.IsBuild()}")
		builtins.print(f"metaPath: {self.__application.GetMetaPath()}")
		builtins.print(f"sourcePath: {self.__application.GetSourcePath()}")
		builtins.print(f"resourcePath: {self.__application.GetResourcePath()}")
		builtins.print(f"workspacePath: {self.__application.GetWorkspacePath()}")

		#--------------------------------------------------------------------------------
		# 실행 방식에 따른 설정.
		# 빌드.
		logType : LogType = LogType.NONE
		if self.Application.PreparedData.Type == ApplicationExecuteType.BUILD:
			builtins.print("__BUILD__")
			logType = LogType.ERROR
		# 서비스.
		elif self.Application.PreparedData.Type == ApplicationExecuteType.SERVICE:
			builtins.print("__SERVICE__")
			logType = LogType.INFO
		# 소스.
		elif self.Application.PreparedData.Type == ApplicationExecuteType.SOURCE:
			builtins.print("__SOURCE__")				
			if isDebug:
				builtins.print("__DEBUG__")
				logType = LogType.DEBUG
			else:
				builtins.print("__NODEBUG__")
				logType = LogType.INFO
		else:
			raise Exception("Unknown Execute Type!!")

		#--------------------------------------------------------------------------------
		# 로그 설정.
		# 순서 : DEBUG < INFO < WARNING < ERROR < CRITICAL.
		try:
			useLogFile : bool = Application.HasSymbol(SYMBOL_LOG)
			if useLogFile:
				logPath = self.__application.GetRootPathWithRelativePath("logs")
				self.__application.Logger.Start(logType, logPath)
			else:
				self.__application.Logger.Start(logType, EMPTY)
		except Exception as exception:
			builtins.print(exception)

		# # 시그널 등록.
		# signal.signal(signal.SIGINT, lambda sight, frame: sys.exit(0))

		#--------------------------------------------------------------------------------
		# 시작.
		try:
			# 잔여 인자 출력.
			if sys.argv:
				Application.Log("__ARGUMENTS__")
				index = 0
				for arg in sys.argv:
					Application.Log(f" - [{index}] {arg}")
					index += 1

			# 실행.
			startModule : ModuleType = importlib.import_module(self.Application.PreparedData.StartModuleName)
			startFunction = builtins.getattr(startModule, self.Application.PreparedData.StartFunctionName)
			exitCode : int = startFunction(sys.argv)
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