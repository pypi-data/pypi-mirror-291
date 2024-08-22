#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_speak.entity import *
from evo_package_speak.utility import *

# ---------------------------------------------------------------------------------------------------------------------------------------
# CSpeakApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""CSpeakApi
"""
class CSpeakApi(CApi):
	__instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self):   
		if CSpeakApi.__instance != None:
			raise Exception("ERROR:SINGLETON")
		else:
			super().__init__()
			CSpeakApi.__instance = self
			self.currentPath = os.path.dirname(os.path.abspath(__file__))
			
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""getInstance Singleton

	Raises:
		Exception:  api exception

	Returns:
		_type_: CSpeakApi instance
	"""
	@staticmethod
	def getInstance():
		if CSpeakApi.__instance is None:
			cObject = CSpeakApi()  
			cObject.doInit()  
		return CSpeakApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doInit

	Raises:
		Exception: api exception

	Returns:

	"""   
	def doInit(self):   
		try:			
			USpeakApi.getInstance().doInit()
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise	  
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doAddApi

	Raises:
		Exception: api exception

	Returns:

	"""
	@override   
	def doAddApi(self):
		try:			
			
			api0 = self.newApi("speak-tts", callback=self.onTts, input=ESpeakInput, output=ESpeakOutput )
			api0.description="speak-tts _DESCRIPTION_"
			api0.required="ESpeakInput.eApiText"

			api1 = self.newApi("speak-stt", callback=self.onStt, input=EApiFile, output=EApiFile )
			api1.description="speak-stt _DESCRIPTION_"
			api1.required="*"

			api2 = self.newApi("speak-get_model", callback=self.onGetModel, input=EApiQuery, output=ESpeakModel )
			api2.description="speak-get_model _DESCRIPTION_"
			api2.required="eApiQuery.eObjectID"

			api3 = self.newApi("speak-query_model", callback=self.onQueryModel, input=EApiQuery, output=ESpeakMapModel )
			api3.description="speak-query_model _DESCRIPTION_"
			api3.required="EApiQuery.query"
  
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onTts api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onTts(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onTts: {eAction} ")

					
			async for eActionOutput in USpeakApi.getInstance().doOnTts(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onStt api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onStt(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onStt: {eAction} ")

					
			async for eActionOutput in USpeakApi.getInstance().doOnStt(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onGetModel api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGetModel(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGetModel: {eAction} ")

					
			async for eActionOutput in USpeakApi.getInstance().doOnGetModel(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onQueryModel api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onQueryModel(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onQueryModel: {eAction} ")

					
			async for eActionOutput in USpeakApi.getInstance().doOnQueryModel(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------
