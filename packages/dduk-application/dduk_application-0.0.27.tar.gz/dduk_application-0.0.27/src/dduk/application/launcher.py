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
	__preparedData : dict


	#--------------------------------------------------------------------------------
	# 애플리케이션 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def Application(self) -> Application:
		return self.__application
	

	#--------------------------------------------------------------------------------
	# 프리페어드 데이터 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def PreparedData(self) -> dict:
		return self.__preparedData
	

	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__preparedData = None
		self.__application = None


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	def Launch(self) -> int:
		builtins.print("__LAUNCH__")

		#--------------------------------------------------------------------------------
		# 빌드 설정.
		isBuild : bool = Launcher.VerifyBuild()
		self.__application.InternalData.SetBuild(isBuild)
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
		prepareFilePath = Application.GetMetaPathWithRelativePath("prepare.yaml")
		with open(prepareFilePath, WRITE, encoding = UTF8) as file:
			yamlString = file.read()
			self.__preparedData = yaml.load(yamlString, Loader = yaml.FullLoader)

		#--------------------------------------------------------------------------------
		# 애플리케이션 셋팅.
		self.__application = Application(self.__preparedData.Name)

		#--------------------------------------------------------------------------------
		# 디버깅 설정. (서비스와 빌드는 디버깅 할 수 없다고 간주한다.)
		isDebug : bool = Launcher.VerifyDebug()
		
		#--------------------------------------------------------------------------------
		# 실행 인수 : 실행된 파일 이름 설정.
		if sys.argv:
			Application.Log("__EXECUTE__")
			executeFileName = sys.argv[0]
			self.__application.InternalData.SetExecuteFileName(executeFileName)
			sys.argv = sys.argv[1:]

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
		# 심볼 및 로그 설정.
		try:
			# 준비 데이터로부터 심볼목록을 불러와 설정.
			if self.__preparedData:					
				Application.Log("__PREPARED_DATA__")
				symbols = self.__preparedData["Symbols"]
				self.__application.InternalData.SetSymbols(symbols)

			# 심볼 변환.
			applicationExecuteType = ApplicationExecuteType.ToValue(self.__preparedData["Type"])

			# 빌드.
			if applicationExecuteType == ApplicationExecuteType.BUILD:
				builtins.print("__BUILD__")
				self.__application.InternalData.SetDebug(False)
			# 서비스.
			elif applicationExecuteType == ApplicationExecuteType.SERVICE:
				builtins.print("__SERVICE__")
				self.__application.InternalData.SetDebug(False)
			# 소스.
			elif applicationExecuteType == ApplicationExecuteType.SOURCE:
				builtins.print("__SOURCE__")				
				if isDebug:
					builtins.print("__DEBUG__")
					self.__application.InternalData.SetDebug(True)
				else:
					builtins.print("__NODEBUG__")
					self.__application.InternalData.SetDebug(False)

				# 로그 설정.
				# 순서 : DEBUG < INFO < WARNING < ERROR < CRITICAL.
				useLog : bool = Application.HasSymbol(SYMBOL_LOG)
				if useLog:
					logPath = self.__application.GetRootPathWithRelativePath("logs")
					self.__application.Logger.Start(LogType.DEBUG, logPath)

		except Exception as exception:
			builtins.print(exception)

		# # 시그널 등록.
		# signal.signal(signal.SIGINT, lambda sight, frame: sys.exit(0))

		#--------------------------------------------------------------------------------
		# 공통 : 인자 및 디버그 설정 및 시작.
		try:
			# 잔여 인자 출력.
			if sys.argv:
				Application.Log("__ARGUMENTS__")
				index = 0
				for arg in sys.argv:
					Application.Log(f" - [{index}] {arg}")
					index += 1

			# 실행.
			module : ModuleType = importlib.import_module(self.__preparedData["StartModuleName"])
			function = builtins.getattr(module, self.__preparedData["StartFunctionName"])
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