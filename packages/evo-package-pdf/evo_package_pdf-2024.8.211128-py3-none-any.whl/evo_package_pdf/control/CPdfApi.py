#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_pdf.entity import *
from evo_package_pdf.utility import *

# ---------------------------------------------------------------------------------------------------------------------------------------
# CPdfApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""CPdfApi
"""
class CPdfApi(CApi):
	__instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self):   
		if CPdfApi.__instance != None:
			raise Exception("ERROR:SINGLETON")
		else:
			super().__init__()
			CPdfApi.__instance = self
			self.currentPath = os.path.dirname(os.path.abspath(__file__))
			
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""getInstance Singleton

	Raises:
		Exception:  api exception

	Returns:
		_type_: CPdfApi instance
	"""
	@staticmethod
	def getInstance():
		if CPdfApi.__instance is None:
			cObject = CPdfApi()  
			cObject.doInit()  
		return CPdfApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doInit

	Raises:
		Exception: api exception

	Returns:

	"""   
	def doInit(self):   
		try:			
			UPdfApi.getInstance().doInit()
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
			
			api0 = self.newApi("pdf-parser", callback=self.onParser, input=EPdfInput, output=EPdfOutput )
			api0.description="pdf-parser description"
			api0.required="*"
  
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onParser api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onParser(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onParser: {eAction} ")

					
			async for eActionOutput in UPdfApi.getInstance().doOnParser(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------
