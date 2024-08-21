#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiFile import EApiFile
#========================================================================================================================================
"""EPdfInput

    this is EPdfInput DESCRIPTION
    
"""
class EPdfInput(EObject):

    VERSION:str="78fd0c3a94a736cc72001287f010b77447d4391fe72148c85bf7201844987f9a"

    def __init__(self):
        super().__init__()
        
        self.pdf:EApiFile = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteEObject(self.pdf, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.pdf = self._doReadEObject(EApiFile, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tpdf:{self.pdf}",
                            ]) 
        return strReturn
    